@echo off
chcp 65001 > nul
echo.
echo ==========================================
echo   嗨萌马短视频创作管家 - 一键启动
echo ==========================================
echo.
echo 正在启动服务，请稍候...
echo.

REM 检查Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python，请先安装Python
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 安装依赖
echo [1/3] 正在安装依赖...
pip install -q -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 启动API服务（后台）
echo [2/3] 正在启动API服务...
start /b python api_server.py > nul 2>&1

REM 等待服务启动
timeout /t 3 /nobreak > nul

REM 打开网页
echo [3/3] 正在打开网页...
start frontend/index.html

echo.
echo ✅ 启动成功！
echo.
echo 📱 浏览器会自动打开网页
echo 💡 如果网页没有自动打开，请手动双击打开 frontend/index.html
echo.
echo ⚠️  请勿关闭此窗口，关闭后服务将停止
echo.
pause
