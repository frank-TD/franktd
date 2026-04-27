@echo off
REM 启动API服务器 (Windows)

echo ==========================================
echo   嗨萌马Agent API服务启动
echo ==========================================
echo.

REM 检查Python版本
echo [1/4] 检查Python版本...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python未安装或未配置环境变量
    pause
    exit /b 1
)

REM 安装依赖
echo.
echo [2/4] 安装依赖...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

REM 创建日志目录
echo.
echo [3/4] 创建日志目录...
if not exist logs mkdir logs

REM 启动服务
echo.
echo [4/4] 启动API服务...
echo.
echo ✅ 服务启动成功！
echo.
echo 📱 访问地址：
echo    - API服务：http://localhost:8000
echo    - API文档：http://localhost:8000/docs
echo    - 前端页面：双击打开 frontend\index.html
echo.
echo 💡 提示：关闭此窗口将停止服务
echo.
echo ==========================================
echo.

python api_server.py

pause
