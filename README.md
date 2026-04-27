# 🎬 嗨萌马短视频创作管家

**智能选题 · 热点捕捉 · 创意生成**

---

## ✨ 功能特性

- 🤖 **智能Agent对话** - 基于LangChain + Coze大模型
- 📊 **多平台热点抓取** - 抖音、微博、小红书
- 🎯 **双赛道选题** - 泛流量热点 + 儿童安全教育
- 🌐 **多种部署方式** - Streamlit Web、API服务、企微机器人
- ⏰ **定时推送** - GitHub Actions定时任务
- 📱 **移动端支持** - 完美适配手机访问

---

## 🚀 快速开始

### 方式1：Streamlit Web界面（推荐新手）

**优势：** 一键部署、无需服务器、支持多人

```bash
# 1. 访问Streamlit Cloud
https://share.streamlit.io

# 2. 使用GitHub登录
# 3. 创建应用，选择 frank-TD/franktd 仓库
# 4. 配置环境变量（COZE_WORKLOAD_IDENTITY_API_KEY、COZE_INTEGRATION_MODEL_BASE_URL）
# 5. 部署成功后访问URL
```

**详细教程：** 查看 [WEB_INTERFACE_DEPLOY.md](WEB_INTERFACE_DEPLOY.md)

---

### 方式2：前端 + API服务（推荐定制）

**优势：** 灵活定制、简单易用、易于部署

**启动API服务：**

**Windows:**
```bash
# 双击运行
scripts\start_api.bat

# 或命令行
python api_server.py
```

**Mac/Linux:**
```bash
chmod +x scripts/start_api.sh
./scripts/start_api.sh

# 或直接
python api_server.py
```

**打开前端页面：**

```bash
# 方式1：直接打开HTML文件
frontend/index.html

# 方式2：使用本地服务器（推荐）
python -m http.server 8080
# 访问：http://localhost:8080/frontend/index.html
```

**详细教程：** 查看 [API_FRONTEND_GUIDE.md](API_FRONTEND_GUIDE.md)

---

### 方式3：企业微信机器人

**优势：** 无需打开网页、直接对话、支持定时推送

**步骤：**
1. 在企业微信创建智能机器人（API模式）
2. 获取Bot ID和Secret
3. 配置环境变量
4. 启动服务或部署到Railway

**详细教程：** 查看 [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

---

### 方式4：GitHub Actions定时推送

**优势：** 自动推送、完全免费、无需维护

**步骤：**
1. 配置GitHub Secrets（WECOM_BOT_ID、WECOM_BOT_SECRET等）
2. 启用GitHub Actions
3. 每天北京时间9:00自动推送选题

**详细教程：** 查看 [DOCS_DAILY_PUSH.md](DOCS_DAILY_PUSH.md)

---

## 📦 项目结构

```
.
├── api_server.py              # FastAPI API服务
├── app.py                     # Streamlit Web界面
├── frontend/                  # 前端网页
│   └── index.html            # 前端页面
├── src/                       # 源代码
│   ├── agents/               # Agent核心逻辑
│   │   └── agent.py         # Agent实现
│   ├── tools/                # 工具定义
│   │   ├── hot_topic_searcher.py      # 热点搜索
│   │   ├── hot_topic_filter.py        # 热点筛选
│   │   ├── wecom_long_connection.py   # 企微长连接
│   │   └── ...              # 其他工具
│   └── storage/              # 存储和记忆
├── scripts/                   # 启动脚本
│   ├── start_api.sh/bat      # API服务启动脚本
│   ├── start_web.sh/bat      # Web界面启动脚本
│   ├── start_wecom_bot.py    # 企微机器人启动脚本
│   └── daily_push.py         # 定时推送脚本
├── config/                    # 配置文件
│   └── agent_llm_config.json # Agent配置
├── .github/workflows/         # GitHub Actions
│   └── daily_topic_push.yml  # 定时推送配置
├── requirements.txt           # Python依赖
├── pyproject.toml            # 项目配置
├── railway.toml              # Railway部署配置
└── docs/                     # 文档（各.md文件）
```

---

## 🔧 环境配置

### 必需环境变量

| 变量名 | 说明 | 获取方式 |
|-------|------|---------|
| `COZE_WORKLOAD_IDENTITY_API_KEY` | Coze API密钥 | Coze工作台 |
| `COZE_INTEGRATION_MODEL_BASE_URL` | Coze API地址 | Coze工作台 |

### 企业微信环境变量（可选）

| 变量名 | 说明 |
|-------|------|
| `WECOM_BOT_ID` | 企业微信机器人ID |
| `WECOM_BOT_SECRET` | 企业微信机器人密钥 |

---

## 📚 文档索引

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 项目说明（本文档） |
| [WEB_INTERFACE_DEPLOY.md](WEB_INTERFACE_DEPLOY.md) | Streamlit部署指南 |
| [API_FRONTEND_GUIDE.md](API_FRONTEND_GUIDE.md) | 前端+API部署指南 |
| [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md) | Railway部署指南 |
| [DOCS_DAILY_PUSH.md](DOCS_DAILY_PUSH.md) | 定时推送指南 |
| [WEB_SOLUTION_GUIDE.md](WEB_SOLUTION_GUIDE.md) | Web方案对比 |
| [GITHUB_PUSH_GUIDE.md](GITHUB_PUSH_GUIDE.md) | GitHub推送指南 |
| [GITHUB_AUTH_FIX.md](GITHUB_AUTH_FIX.md) | GitHub认证修复 |

---

## 🎯 使用场景

### 团队协作

**需求：** 团队成员需要获取选题建议

**方案：**
- 内部使用：Streamlit Web或前端+API
- 外部客户：部署到生产环境
- 移动办公：响应式设计，手机可用

### 定时推送

**需求：** 每天自动推送选题清单

**方案：** GitHub Actions定时任务

**效果：** 每天9:00自动推送到企业微信

### 快速测试

**需求：** 快速验证想法

**方案：** 本地运行，立即测试

---

## 💡 快捷问题

Agent支持以下快捷问题：

1. **生成今日选题清单** - 生成当天的选题建议
2. **搜索抖音热门话题** - 抓取抖音热门话题
3. **分析儿童安全教育方向** - 分析儿童安全相关的选题
4. **优化这个选题** - 优化用户提供的选题
5. **推荐泛流量爆款选题** - 推荐可能爆火的选题

---

## 🔒 安全性

- ✅ 对话记录保存在本地浏览器（前端）
- ✅ 环境变量不提交到代码库
- ✅ 支持私有仓库
- ✅ 可添加API密钥认证

---

## 📊 性能

| 方案 | 响应速度 | 并发支持 | 费用 |
|------|---------|---------|------|
| Streamlit Cloud | 快 | 10+ | 完全免费 |
| 前端+API | 快 | 高 | 完全免费 |
| Railway | 快 | 中等 | 完全免费 |
| 本地运行 | 最快 | 低 | 完全免费 |

---

## 🛠️ 开发

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
python -m pytest tests/
```

### 代码规范

```bash
# 使用black格式化
black .

# 使用pylint检查
pylint src/
```

---

## 📞 技术支持

- **GitHub Issues**: 提交问题反馈
- **项目文档**: 查看各.md文件
- **技术栈**:
  - LangChain 1.0
  - LangGraph 1.0
  - Coze大模型
  - FastAPI
  - Streamlit

---

## 🤝 贡献

欢迎贡献代码、提出建议、报告问题！

---

## 📄 许可证

MIT License

---

## 🎉 开始使用

**推荐新手使用Streamlit：**
1. 访问 https://share.streamlit.io
2. 登录并创建应用
3. 配置环境变量
4. 5分钟内完成部署

**推荐开发者使用API：**
1. 启动API服务
2. 打开前端页面
3. 开始对话

**需要定时推送：**
1. 配置GitHub Secrets
2. 启用GitHub Actions
3. 每天自动推送

---

**让团队成员轻松访问Agent吧！** 🚀
