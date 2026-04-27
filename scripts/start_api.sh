#!/bin/bash
# 启动API服务器

echo "=========================================="
echo "  嗨萌马Agent API服务启动"
echo "=========================================="
echo ""

# 检查Python版本
echo "🔍 检查Python版本..."
python3 --version || python --version

# 安装依赖
echo ""
echo "📦 安装依赖..."
pip install -r requirements.txt

# 创建日志目录
echo ""
echo "📁 创建日志目录..."
mkdir -p logs

# 启动服务
echo ""
echo "🚀 启动API服务..."
echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📱 访问地址："
echo "   - API服务：http://localhost:8000"
echo "   - API文档：http://localhost:8000/docs"
echo "   - 前端页面：打开 frontend/index.html"
echo ""
echo "💡 提示：按 Ctrl+C 停止服务"
echo ""
echo "=========================================="

python api_server.py
