# 📌 嗨萌马每日选题定时推送

**完全免费 · 无需服务器 · 自动化推送**

---

## 🎯 功能介绍

- ✅ **自动生成选题**：每天自动抓取抖音、微博、小红书热点
- ✅ **双赛道模式**：泛流量热点选题 + 儿童安全教育选题
- ✅ **定时推送**：支持自定义推送时间
- ✅ **企微集成**：自动推送到企业微信群聊
- ✅ **完全免费**：基于GitHub Actions，无需购买服务器

---

## 🚀 快速开始（5分钟部署）

### 方案1：GitHub Actions定时推送（推荐）

**适用场景**：
- 想要每天自动推送（如每天9:00）
- 不想购买服务器
- 想要完全免费的解决方案

**部署步骤**：

#### 1️⃣ 创建GitHub仓库

```bash
# 如果还没有GitHub账号，先注册：https://github.com

# 将项目推送到GitHub
cd /workspace/projects
git init
git add .
git commit -m "feat: 添加定时推送功能"

# 创建远程仓库后，关联仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git
git branch -M main
git push -u origin main
```

#### 2️⃣ 配置Secrets

进入GitHub仓库，点击：
`Settings` → `Secrets and variables` → `Actions` → `New repository secret`

添加以下4个Secrets：

| Secret名称 | Secret值 | 说明 |
|-----------|---------|------|
| `WECOM_BOT_ID` | `aibylL5aVP4HUVHdyCZfVQzdEUa-FNmAwas` | 企业微信机器人ID |
| `WECOM_BOT_SECRET` | `yTNzMOuXQpXBk8ldjfVne1BetWcB4O8eJu87LxvWWto` | 企业微信机器人密钥 |
| `COZE_WORKLOAD_IDENTITY_API_KEY` | *你的API Key* | Coze API密钥 |
| `COZE_INTEGRATION_MODEL_BASE_URL` | *你的Base URL* | Coze API地址 |

**⚠️ 重要提示**：
- `COZE_WORKLOAD_IDENTITY_API_KEY` 和 `COZE_INTEGRATION_MODEL_BASE_URL` 需要从当前环境获取
- 在Coze工作台找到你的API配置信息

#### 3️⃣ 启用GitHub Actions

推送代码后，GitHub Actions会自动运行：
1. 进入 `Actions` 标签页
2. 选择 `嗨萌马每日选题定时推送` workflow
3. 点击 `Enable workflow`

#### 4️⃣ 手动触发测试

在 `Actions` 页面：
1. 选择 `嗨萌马每日选题定时推送`
2. 点击 `Run workflow` 按钮
3. 选择分支，点击 `Run workflow` 开始运行
4. 等待运行完成，查看日志

#### 5️⃣ 查看推送结果

推送成功后，会在企业微信群聊收到消息：
```
📌 嗨萌马每日选题清单

生成时间：2025年01月15日 09:00

---
# 专题A：泛流量热点选题

## 1. 选题标题
**热点来源：** 抖音
**创意方向：** ...
**预估热度：** 🔥🔥🔥🔥🔥
**推荐理由：** ...
---
...
```

---

### 方案2：本地手动推送

**适用场景**：
- 想要手动控制推送时间
- 测试推送功能
- 紧急推送

**使用方法**：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 设置环境变量（可选，代码中有默认值）
export WECOM_BOT_ID="aibylL5aVP4HUVHdyCZfVQzdEUa-FNmAwas"
export WECOM_BOT_SECRET="yTNzMOuXQpXBk8ldjfVne1BetWcB4O8eJu87LxvWWto"

# 3. 运行推送脚本
python scripts/daily_push.py
```

**输出示例**：
```
============================================================
嗨萌马每日选题推送服务
============================================================
📅 推送时间：2025-01-15 09:00:00
🤖 机器人ID：aibylL5aVP4HUVHdyCZfV...

============================================================
步骤1：生成选题清单
============================================================
🔄 正在初始化Agent...
🔄 正在生成选题清单...
✓ 选题生成成功

============================================================
步骤2：推送到企业微信
============================================================
✓ Access token获取成功，有效期：7200秒
✓ Markdown消息发送成功

============================================================
推送完成
============================================================
✅ 推送成功！
📊 消息ID: xxxxxxxxxx
```

---

### 方案3：服务器定时任务（Crontab）

**适用场景**：
- 有自己的服务器
- 想要更灵活的定时控制
- 需要运行多个定时任务

**部署步骤**：

```bash
# 1. 上传代码到服务器
scp -r /workspace/projects user@your-server:/home/user/

# 2. SSH登录服务器
ssh user@your-server

# 3. 安装依赖
cd ~/projects
pip install -r requirements.txt

# 4. 添加定时任务
crontab -e

# 添加以下内容（每天9:00执行）
0 9 * * * cd /home/user/projects && python scripts/daily_push.py >> logs/cron.log 2>&1

# 5. 查看定时任务
crontab -l
```

---

## 📝 自定义配置

### 修改推送时间

编辑 `.github/workflows/daily_topic_push.yml`：

```yaml
# 默认：每天北京时间9:00（UTC时间1:00）
schedule:
  - cron: '0 1 * * *'

# 示例1：每天北京时间8:00
schedule:
  - cron: '0 0 * * *'

# 示例2：每天北京时间12:00
schedule:
  - cron: '0 4 * * *'

# 示例3：每周一至周五上午9:00
schedule:
  - cron: '0 1 * * 1-5'
```

**Cron时间说明**：
- 格式：`分 时 日 月 周`
- 时区：UTC时间（北京时间 = UTC + 8）
- 示例：
  - `0 1 * * *` = 每天1:00 UTC = 9:00 北京时间
  - `0 0 * * 1-5` = 每天0:00 UTC = 8:00 北京时间（周一至周五）

### 修改推送内容

编辑 `scripts/daily_push.py` 中的 `generate_daily_topic()` 函数：

```python
def generate_daily_topic() -> str:
    prompt = """请为我生成今日的短视频选题清单...

    # 自定义你的提示词
    - 修改专题数量
    - 修改选题类型
    - 修改格式要求
    ...
    """
```

### 添加多个推送时间

编辑 `.github/workflows/daily_topic_push.yml`：

```yaml
on:
  schedule:
    # 每天9:00推送
    - cron: '0 1 * * *'
    # 每天12:00推送
    - cron: '0 4 * * *'
    # 每天18:00推送
    - cron: '0 10 * * *'
```

---

## 🔍 故障排查

### 问题1：GitHub Actions运行失败

**查看日志**：
1. 进入 `Actions` 页面
2. 点击失败的workflow运行
3. 查看详细日志

**常见错误**：
- ❌ `ModuleNotFoundError`: 检查 `requirements.txt` 是否包含所有依赖
- ❌ `API Key无效`: 检查Secrets配置是否正确
- ❌ `Access Token获取失败`: 检查Bot ID和Secret是否正确

### 问题2：企业微信未收到消息

**检查项**：
1. ✅ 机器人是否已添加到群聊
2. ✅ Bot ID和Secret是否正确
3. ✅ 网络连接是否正常
4. ✅ 查看日志是否有错误信息

### 问题3：选题生成失败

**检查项**：
1. ✅ Coze API配置是否正确
2. ✅ 热点数据源是否可用
3. ✅ 网络连接是否正常
4. ✅ 查看日志中的错误信息

---

## 📊 使用统计

**GitHub Actions使用情况**：
- 免费额度：每月2000分钟
- 推送一次：约2-3分钟
- 每月推送30次：约90分钟 ✅ 完全免费

**成本计算**：
- 超出免费额度后：$0.008/分钟
- 每月推送30次：约 $0.72
- 每年成本：约 $8.64

---

## 🎉 成功案例

### 使用场景1：团队协作

```
场景：短视频创作团队
需求：每天上午9:00自动推送选题清单
效果：
✅ 团队成员早上到公司就能看到选题
✅ 节省了人工筛选热点的时间
✅ 提升了内容创作效率
```

### 使用场景2：个人创作者

```
场景：个人短视频创作者
需求：每天获取灵感，不遗漏热点
效果：
✅ 自动推送热点选题，不错过机会
✅ 不需要每天手动搜索热点
✅ 专注于内容创作
```

### 使用场景3：工作室运营

```
场景：短视频工作室
需求：多账号运营，统一选题
效果：
✅ 统一的选题来源
✅ 批量分发到多个群聊
✅ 规范化选题流程
```

---

## 📞 技术支持

如有问题，请检查：
1. 📖 本文档的故障排查部分
2. 🔍 GitHub Actions运行日志
3. 📝 `logs/daily_push.log` 本地日志

---

## 📄 许可证

MIT License

---

**🎊 现在就开始使用吧！**
