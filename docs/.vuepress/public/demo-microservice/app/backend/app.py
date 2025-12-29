#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask 后端 API 服务
提供用户管理的 RESTful API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import redis
import os
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 从环境变量读取配置
MYSQL_HOST = os.getenv('MYSQL_HOST', 'mysql-service')
MYSQL_USER = os.getenv('MYSQL_USER', 'demo_user')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'demo_password')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'demo_db')
REDIS_HOST = os.getenv('REDIS_HOST', 'redis-service')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

# Redis 连接
try:
    redis_client = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        decode_responses=True,
        socket_connect_timeout=5
    )
    redis_client.ping()
    logger.info(f"成功连接到 Redis: {REDIS_HOST}:{REDIS_PORT}")
except Exception as e:
    logger.warning(f"无法连接到 Redis: {e}")
    redis_client = None


def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5
        )
        return connection
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        raise


def init_database():
    """初始化数据库表"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info("数据库表初始化成功")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")


# 应用启动时初始化数据库
init_database()


@app.route('/')
def index():
    """首页"""
    return jsonify({
        'message': 'Welcome to Demo API',
        'version': '1.0.0',
        'endpoints': {
            'health': '/api/health',
            'users': '/api/users',
            'user_detail': '/api/users/<id>'
        }
    })


@app.route('/api/health')
def health():
    """健康检查"""
    health_status = {
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {}
    }
    
    # 检查 MySQL
    try:
        conn = get_db_connection()
        conn.close()
        health_status['services']['mysql'] = 'connected'
    except Exception as e:
        health_status['services']['mysql'] = f'error: {str(e)}'
        health_status['status'] = 'degraded'
    
    # 检查 Redis
    try:
        if redis_client:
            redis_client.ping()
            health_status['services']['redis'] = 'connected'
        else:
            health_status['services']['redis'] = 'not configured'
    except Exception as e:
        health_status['services']['redis'] = f'error: {str(e)}'
    
    return jsonify(health_status)


@app.route('/api/users', methods=['GET'])
def get_users():
    """获取所有用户"""
    try:
        # 尝试从缓存获取
        if redis_client:
            cached_users = redis_client.get('users:all')
            if cached_users:
                logger.info("从缓存返回用户列表")
                return jsonify({
                    'success': True,
                    'data': json.loads(cached_users),
                    'from_cache': True
                })
        
        # 从数据库查询
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY id DESC")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # 缓存结果（60秒）
        if redis_client:
            redis_client.setex('users:all', 60, json.dumps(users, default=str))
        
        logger.info(f"从数据库返回 {len(users)} 个用户")
        return jsonify({
            'success': True,
            'data': users,
            'from_cache': False
        })
    except Exception as e:
        logger.error(f"获取用户列表失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """获取单个用户"""
    try:
        # 尝试从缓存获取
        cache_key = f'user:{user_id}'
        if redis_client:
            cached_user = redis_client.get(cache_key)
            if cached_user:
                logger.info(f"从缓存返回用户 {user_id}")
                return jsonify({
                    'success': True,
                    'data': json.loads(cached_user),
                    'from_cache': True
                })
        
        # 从数据库查询
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        # 缓存结果（60秒）
        if redis_client:
            redis_client.setex(cache_key, 60, json.dumps(user, default=str))
        
        logger.info(f"从数据库返回用户 {user_id}")
        return jsonify({
            'success': True,
            'data': user,
            'from_cache': False
        })
    except Exception as e:
        logger.error(f"获取用户失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users', methods=['POST'])
def create_user():
    """创建用户"""
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({
                'success': False,
                'error': 'Name and email are required'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s)",
            (data['name'], data['email'])
        )
        conn.commit()
        user_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        # 清除缓存
        if redis_client:
            redis_client.delete('users:all')
        
        logger.info(f"创建用户成功: {user_id}")
        return jsonify({
            'success': True,
            'data': {
                'id': user_id,
                'name': data['name'],
                'email': data['email']
            }
        }), 201
    except pymysql.IntegrityError:
        return jsonify({
            'success': False,
            'error': 'Email already exists'
        }), 409
    except Exception as e:
        logger.error(f"创建用户失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """更新用户"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided'
            }), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 构建更新语句
        updates = []
        params = []
        if 'name' in data:
            updates.append("name = %s")
            params.append(data['name'])
        if 'email' in data:
            updates.append("email = %s")
            params.append(data['email'])
        
        if not updates:
            return jsonify({
                'success': False,
                'error': 'No valid fields to update'
            }), 400
        
        params.append(user_id)
        sql = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(sql, params)
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        cursor.close()
        conn.close()
        
        # 清除缓存
        if redis_client:
            redis_client.delete('users:all')
            redis_client.delete(f'user:{user_id}')
        
        logger.info(f"更新用户成功: {user_id}")
        return jsonify({
            'success': True,
            'message': 'User updated successfully'
        })
    except pymysql.IntegrityError:
        return jsonify({
            'success': False,
            'error': 'Email already exists'
        }), 409
    except Exception as e:
        logger.error(f"更新用户失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """删除用户"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        
        if cursor.rowcount == 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'error': 'User not found'
            }), 404
        
        cursor.close()
        conn.close()
        
        # 清除缓存
        if redis_client:
            redis_client.delete('users:all')
            redis_client.delete(f'user:{user_id}')
        
        logger.info(f"删除用户成功: {user_id}")
        return jsonify({
            'success': True,
            'message': 'User deleted successfully'
        })
    except Exception as e:
        logger.error(f"删除用户失败: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
