#!/bin/bash
# 嗨萌马短视频创作管家 - 一键启动脚本

echo ""
echo "=========================================="
echo "  嗨萌马短视频创作管家 - 一键启动"
echo "=========================================="
echo ""
echo "正在启动服务，请稍候..."
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 未检测到Python，请先安装Python"
        echo "下载地址：https://www.python.org/downloads/"
        exit 1
    else
        PYTHON=python
    fi
else
    PYTHON=python3
fi

# 安装依赖
echo "[1/3] 正在安装依赖..."
$PYTHON -m pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 启动API服务（后台）
echo "[2/3] 正在启动API服务..."
$PYTHON api_server.py > /dev/null 2>&1 &
API_PID=$!

# 等待服务启动
sleep 3

# 打开网页
echo "[3/3] 正在打开网页..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open frontend/index.html
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open frontend/index.html
else
    echo "请手动打开网页：frontend/index.html"
fi

echo ""
echo "✅ 启动成功！"
echo ""
echo "📱 浏览器会自动打开网页"
echo "💡 如果网页没有自动打开，请手动打开 frontend/index.html"
echo ""
echo "⚠️  请勿关闭此窗口，关闭后服务将停止"
echo ""
echo "按 Ctrl+C 停止服务"
echo ""

# 等待API进程
wait $API_PID
