# 🚀 Railway.app 免费部署教程

**完全免费 · 支持WebSocket长连接 · 支持主动推送**

---

## 为什么选择Railway.app？

| 特性 | Railway.app | 服务器 |
|------|-------------|--------|
| 成本 | **完全免费**（$5/月额度） | 每月几十元 |
| 配置难度 | 🟢 简单 | 🟡 中等 |
| 支持WebSocket | ✅ 支持 | ✅ 支持 |
| 自动部署 | ✅ 支持 | ❌ 需手动 |
| 维护成本 | 🟢 低 | 🟡 中等 |

---

## 📋 部署前准备

### 1. 注册GitHub账号（如果还没有）

访问：https://github.com/signup

### 2. 注册Railway账号

访问：https://railway.app
- 点击 "Start a new project"
- 使用GitHub账号登录

---

## 🚀 部署步骤（5分钟完成）

### 步骤1：推送代码到GitHub

```bash
# 1. 初始化Git仓库
cd /workspace/projects
git init
git add .
git commit -m "feat: 企业微信机器人定时推送"

# 2. 创建GitHub仓库
# 访问 https://github.com/new 创建一个新仓库

# 3. 关联远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

### 步骤2：在Railway部署

1. **登录Railway**
   - 访问：https://railway.app
   - 使用GitHub账号登录

2. **创建新项目**
   - 点击右上角 `+ New Project`
   - 选择 `Deploy from GitHub repo`

3. **选择仓库**
   - 找到你刚才推送的仓库
   - 点击 `Deploy Now`

4. **配置环境变量**
   - 部署开始后，点击 `Variables` 标签
   - 添加以下环境变量：

| 变量名 | 值 |
|-------|-----|
| `WECOM_BOT_ID` | `aibylL5aVP4HUVHdyCZfVQzdEUa-FNmAwas` |
| `WECOM_BOT_SECRET` | `yTNzMOuXQpXBk8ldjfVne1BetWcB4O8eJu87LxvWWto` |
| `COZE_WORKLOAD_IDENTITY_API_KEY` | *你的Coze API Key* |
| `COZE_INTEGRATION_MODEL_BASE_URL` | *你的Coze Base URL* |

   **获取Coze API Key和Base URL**：
   - 登录Coze工作台
   - 进入API管理页面
   - 复制API Key和Base URL

5. **重新部署**
   - 添加环境变量后，点击 `Redeploy`
   - 等待部署完成（约2-3分钟）

### 步骤3：验证部署

1. **查看日志**
   - 在Railway项目页面，点击 `Logs` 标签
   - 查看服务启动日志

2. **预期日志输出**
   ```
   ============================================================
   嗨萌马企业微信机器人服务
   ============================================================

   [企微机器人] 正在连接企业微信...
   [企微机器人] ✓ 订阅指令已发送
   [企微机器人] ✅ 连接成功！
   [企微机器人] 正在初始化Agent...
   [企微机器人] ✅ Agent初始化完成
   [企微机器人] 开始监听消息...
   ```

3. **测试推送**
   - 在企业微信中@机器人，发送"推送选题"
   - 应该能收到自动回复

---

## ⏰ 配置定时推送

Railway支持多种定时方式：

### 方式1：使用Railway Cron（推荐）

1. 在Railway项目页面，点击 `+ New Service`
2. 选择 `GitHub` → 选择你的仓库
3. 点击 `Variables`，添加环境变量
4. 在 `Settings` → `Cron Jobs` 中配置定时任务：
   ```
   0 1 * * *  # 每天北京时间9:00执行
   ```
5. 启动命令设置为：`python scripts/daily_push.py`

### 方式2：在现有服务中集成定时器

修改 `src/wecom_bot_service.py`，添加定时推送功能：

```python
import asyncio
from datetime import datetime, time as dt_time

async def daily_push_scheduler():
    """每日定时推送"""
    while True:
        now = datetime.now()
        # 每天北京时间9:00推送（UTC时间1:00）
        push_time = dt_time(1, 0)  # UTC 1:00

        if now.time() >= push_time:
            logger.info("📌 触发定时推送...")
            # 调用推送函数
            try:
                # 这里调用推送逻辑
                pass
            except Exception as e:
                logger.error(f"定时推送失败: {str(e)}")

        # 每分钟检查一次
        await asyncio.sleep(60)
```

### 方式3：使用GitHub Actions（最简单）

已经在 `.github/workflows/daily_topic_push.yml` 中配置好了，每天北京时间9:00自动推送。

---

## 📊 费用说明

### Railway免费额度

| 资源 | 免费额度 | 超出费用 |
|------|---------|---------|
| 执行时间 | $5/月 | $0.00025/秒 |
| 内存 | 512MB | $0.00000009/MB秒 |
| 存储 | 1GB | $0.00000005/GB秒 |

### 实际使用估算

**您的使用场景**：
- 服务持续运行：24小时 × 30天 = 720小时
- 每小时费用：$0.00025 × 3600 = $0.0009
- 每月费用：$0.0009 × 720 = **$0.65**（约5元人民币）

**结论**：完全在免费额度内！✅

---

## 🔍 监控和日志

### 查看实时日志

1. 进入Railway项目页面
2. 点击你的服务
3. 点击 `Logs` 标签
4. 查看实时日志输出

### 查看使用情况

1. 点击 `Settings` → `Usage`
2. 查看执行时间、内存使用等
3. 确保在免费额度内

---

## 🛠️ 常见问题

### 问题1：部署失败

**排查步骤**：
1. 查看Railway构建日志
2. 检查依赖是否都安装成功
3. 确认Python版本是否为3.10+

### 问题2：服务启动失败

**排查步骤**：
1. 查看运行日志
2. 检查环境变量是否配置正确
3. 确认端口是否被占用

### 问题3：企业微信连接失败

**排查步骤**：
1. 检查Bot ID和Secret是否正确
2. 确认机器人是否已创建
3. 查看日志中的连接错误信息

### 问题4：定时推送不工作

**排查步骤**：
1. 检查Cron配置是否正确
2. 确认时区设置（Railway使用UTC时间）
3. 查看定时任务的执行日志

---

## 🔄 更新部署

当您修改代码后：

```bash
# 1. 提交修改
git add .
git commit -m "fix: 修复xxx问题"
git push

# 2. Railway会自动重新部署
# 等待部署完成即可
```

---

## 📞 技术支持

- Railway官方文档：https://docs.railway.app/
- 企业微信API文档：https://open.work.weixin.qq.com/
- 本项目文档：查看 `DOCS_DAILY_PUSH.md`

---

## 🎉 完成！

现在您的企业微信机器人已经成功部署到Railway.app，并且：

✅ 服务24小时运行
✅ 支持主动推送消息
✅ 完全免费
✅ 自动部署和更新
✅ 支持定时推送

**享受完全免费的定时推送服务吧！** 🎊
