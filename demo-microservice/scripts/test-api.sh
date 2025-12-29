#!/bin/bash
# API 测试脚本

set -e

API_URL="http://demo.local/api"

echo "======================================"
echo "开始测试 API..."
echo "======================================"

# 检查 API 健康状态
echo ""
echo "1. 检查 API 健康状态..."
curl -s "$API_URL/health" | python3 -m json.tool

# 获取所有用户
echo ""
echo "2. 获取所有用户..."
curl -s "$API_URL/users" | python3 -m json.tool

# 创建用户
echo ""
echo "3. 创建新用户..."
curl -s -X POST "$API_URL/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@example.com"}' | python3 -m json.tool

echo ""
echo "4. 创建第二个用户..."
curl -s -X POST "$API_URL/users" \
  -H "Content-Type: application/json" \
  -d '{"name":"李四","email":"lisi@example.com"}' | python3 -m json.tool

# 再次获取所有用户
echo ""
echo "5. 再次获取所有用户..."
curl -s "$API_URL/users" | python3 -m json.tool

# 获取单个用户
echo ""
echo "6. 获取用户 ID=1..."
curl -s "$API_URL/users/1" | python3 -m json.tool

# 更新用户
echo ""
echo "7. 更新用户 ID=1..."
curl -s -X PUT "$API_URL/users/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"张三","email":"zhangsan@updated.com"}' | python3 -m json.tool

# 验证更新
echo ""
echo "8. 验证更新后的用户..."
curl -s "$API_URL/users/1" | python3 -m json.tool

# 删除用户
echo ""
echo "9. 删除用户 ID=2..."
curl -s -X DELETE "$API_URL/users/2" | python3 -m json.tool

# 最终用户列表
echo ""
echo "10. 最终用户列表..."
curl -s "$API_URL/users" | python3 -m json.tool

echo ""
echo "======================================"
echo "API 测试完成！"
echo "======================================"
