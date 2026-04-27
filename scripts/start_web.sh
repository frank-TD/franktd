#!/bin/bash
# Streamlit Web界面启动脚本

echo "=========================================="
echo "  嗨萌马短视频创作管家 - Web界面启动"
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

# 启动Streamlit
echo ""
echo "🚀 启动Streamlit服务..."
echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📱 访问地址："
echo "   - 本地访问：http://localhost:8501"
echo "   - 局域网访问：http://$(hostname -I | awk '{print $1}'):8501"
echo ""
echo "💡 提示：按 Ctrl+C 停止服务"
echo ""
echo "=========================================="

streamlit run app.py
