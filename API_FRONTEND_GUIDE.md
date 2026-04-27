# 🌐 前端 + API 服务部署指南

**通过API方式接入Agent，让同事通过网页对话**

---

## 🎯 方案说明

### 架构设计

```
前端 (HTML/JavaScript)
    ↓ HTTP请求
API服务 (FastAPI)
    ↓ 调用
Agent (LangChain)
    ↓
回复
```

### 优势

✅ **简单易用**
- 前端只需HTML + JavaScript
- 无需复杂的前端框架

✅ **灵活部署**
- API可以部署在任何服务器
- 前端可以部署在任何地方

✅ **易于定制**
- 可以自定义前端样式
- 可以添加新功能

✅ **性能优秀**
- API异步处理
- 支持并发访问

---

## 📦 已创建的文件

### 后端文件
- ✅ `api_server.py` - FastAPI API服务
- ✅ `requirements.txt` - 依赖文件（已更新）

### 前端文件
- ✅ `frontend/index.html` - 前端网页

### 启动脚本
- ✅ `scripts/start_api.sh` - Mac/Linux启动脚本
- ✅ `scripts/start_api.bat` - Windows启动脚本

---

## 🚀 快速开始（5分钟）

### 方式1：本地运行

#### 步骤1：启动API服务

**Windows:**
```bash
# 双击运行
scripts\start_api.bat

# 或命令行
pip install -r requirements.txt
python api_server.py
```

**Mac/Linux:**
```bash
chmod +x scripts/start_api.sh
./scripts/start_api.sh

# 或直接
python api_server.py
```

#### 步骤2：打开前端页面

**方式1：直接打开HTML文件**
```bash
# 双击打开
frontend/index.html
```

**方式2：使用本地服务器（推荐）**
```bash
# 使用Python启动
python -m http.server 8080

# 然后访问
http://localhost:8080/frontend/index.html
```

#### 步骤3：开始使用

1. 打开前端页面
2. 等待"服务已连接"
3. 输入问题或点击快捷问题
4. 查看Agent回复

---

### 方式2：部署到服务器

#### 步骤1：部署API服务

**方法1：Railway.app（推荐）**

1. **创建Procfile**
```bash
# 在项目根目录创建或更新 Procfile
web: uvicorn api_server:app --host 0.0.0.0 --port 8000
```

2. **部署到Railway**
   - 访问：https://railway.app
   - 创建项目，选择 `frank-TD/franktd` 仓库
   - 配置环境变量（与之前相同）
   - 点击 Deploy

3. **获取API地址**
   - 部署成功后，Railway会提供一个URL
   - 例如：`https://your-app.railway.app`

**方法2：使用自己的服务器**

```bash
# 1. 上传代码到服务器
scp -r /workspace/projects user@your-server:/home/user/

# 2. SSH登录服务器
ssh user@your-server

# 3. 安装依赖
cd ~/projects
pip install -r requirements.txt

# 4. 启动API服务（后台运行）
nohup python api_server.py > logs/api.log 2>&1 &

# 5. 查看日志
tail -f logs/api.log
```

#### 步骤2：修改前端API地址

**本地修改：**
```javascript
// 打开 frontend/index.html
// 找到这一行
const API_URL = 'http://localhost:8000/api/chat';

// 修改为服务器地址
const API_URL = 'https://your-app.railway.app/api/chat';

// 同时修改健康检查地址
const HEALTH_URL = 'https://your-app.railway.app/health';
```

**部署前端：**

**选项1：部署到静态托管（推荐）**

1. **使用GitHub Pages（免费）**
   - 将 `frontend` 目录推送到GitHub
   - 开启GitHub Pages
   - 获取访问地址

2. **使用Netlify（免费）**
   - 访问：https://netlify.com
   - 拖拽 `frontend` 目录上传
   - 立即获得访问地址

3. **使用Vercel（免费）**
   - 访问：https://vercel.com
   - 导入项目或拖拽上传
   - 立即获得访问地址

**选项2：直接使用HTML文件**
- 将 `frontend/index.html` 发给同事
- 同事直接用浏览器打开

---

## 🔌 API接口说明

### 1. 健康检查

**请求：**
```http
GET /health
```

**响应：**
```json
{
  "status": "healthy",
  "agent": "ready"
}
```

### 2. 对话接口

**请求：**
```http
POST /api/chat
Content-Type: application/json

{
  "message": "生成今日选题清单",
  "session_id": "session_20260427_123456"
}
```

**响应：**
```json
{
  "message": "这里是Agent的回复内容...",
  "timestamp": "2026-04-27 16:30:00",
  "session_id": "session_20260427_123456"
}
```

### 3. 获取API信息

**请求：**
```http
GET /api/info
```

**响应：**
```json
{
  "service": "嗨萌马Agent API",
  "version": "1.0.0",
  "features": [
    "与Agent对话",
    "支持会话管理",
    "跨域访问"
  ],
  "endpoints": {
    "POST /api/chat": "与Agent对话",
    "GET /api/info": "获取API信息",
    "GET /health": "健康检查"
  }
}
```

---

## 🎨 前端定制

### 修改样式

打开 `frontend/index.html`，修改CSS部分：

```css
/* 修改主题颜色 */
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* 修改为其他颜色 */
.header {
    background: linear-gradient(135deg, #ff6b6b 0%, #feca57 100%);
}
```

### 添加新功能

**示例：添加导出对话功能**

```javascript
// 在 frontend/index.html 中添加
function exportConversation() {
    const messages = document.querySelectorAll('.message');
    let content = '';

    messages.forEach(msg => {
        const role = msg.classList.contains('user') ? '用户' : '嗨萌马';
        const text = msg.lastElementChild.textContent;
        content += `${role}: ${text}\n\n`;
    });

    // 下载文件
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `对话_${new Date().toISOString().slice(0,10)}.txt`;
    a.click();
}

// 在HTML中添加按钮
<button onclick="exportConversation()">导出对话</button>
```

---

## 🔐 安全性

### 生产环境配置

**1. 启用HTTPS**
```python
# 在 api_server.py 中
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_certfile="cert.pem", ssl_keyfile="key.pem")
```

**2. 限制CORS**
```python
# 在 api_server.py 中
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # 只允许特定域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**3. 添加API密钥认证**
```python
# 在 api_server.py 中添加
API_KEY = os.getenv("API_KEY")

@app.middleware("http")
async def verify_api_key(request: Request, call_next):
    if request.url.path != "/health":  # 健康检查不需要认证
        api_key = request.headers.get("X-API-Key")
        if api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Invalid API Key")
    return await call_next(request)
```

---

## 📊 性能优化

### 1. 使用缓存

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_response(message: str):
    """缓存常见问题的回复"""
    # 实现缓存逻辑
    pass
```

### 2. 异步处理

```python
from fastapi import BackgroundTasks

async def chat_async(request: ChatRequest, background_tasks: BackgroundTasks):
    """异步处理对话请求"""
    # 实现异步逻辑
    pass
```

### 3. 使用消息队列

对于高并发场景，可以使用Celery + Redis：
```python
from celery import Celery

celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def process_message_async(message: str, session_id: str):
    """异步处理消息"""
    # 实现异步处理逻辑
    pass
```

---

## 🛠️ 故障排查

### 问题1：前端无法连接API

**检查项：**
1. API服务是否启动
2. API地址是否正确
3. 网络是否可达
4. 浏览器控制台是否有错误

**解决方案：**
```bash
# 检查API服务
curl http://localhost:8000/health

# 查看API日志
tail -f logs/api.log
```

### 问题2：Agent初始化失败

**检查项：**
1. 环境变量是否配置
2. Coze API Key是否正确
3. 网络连接是否正常

**解决方案：**
```bash
# 检查环境变量
echo $COZE_WORKLOAD_IDENTITY_API_KEY
echo $COZE_INTEGRATION_MODEL_BASE_URL

# 测试Coze API
curl -X POST https://api.coze.cn/v3/chat/completions \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### 问题3：响应速度慢

**优化建议：**
1. 使用异步处理
2. 添加缓存机制
3. 优化Agent提示词
4. 使用更快的模型

---

## 🎯 使用场景

### 场景1：团队内部使用

```
需求：团队成员在不同地点访问
方案：API部署到服务器，前端部署到静态托管
效果：
✅ 任何地方都能访问
✅ 响应速度快
✅ 易于维护
```

### 场景2：外部客户使用

```
需求：客户需要在线咨询
方案：API部署到生产环境，前端部署到CDN
效果：
✅ 全球加速访问
✅ 高可用性
✅ 安全可靠
```

### 场景3：移动端使用

```
需求：支持手机访问
方案：前端响应式设计，已适配移动端
效果：
✅ 手机完美显示
✅ 触控友好
✅ 加载快速
```

---

## 📞 技术支持

- **FastAPI文档**: https://fastapi.tiangolo.com/
- **项目文档**: 查看其他.md文件
- **问题反馈**: 提交Issue

---

## 🎊 开始使用

1. **启动API服务**
   - 本地：`python api_server.py`
   - 服务器：部署到Railway或自己的服务器

2. **打开前端页面**
   - 本地：打开 `frontend/index.html`
   - 在线：部署到GitHub Pages/Netlify

3. **开始对话**
   - 输入问题
   - 查看回复

---

**享受简单易用的Web对话界面吧！** 🚀
