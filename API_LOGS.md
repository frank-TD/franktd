# 📊 API调用日志查询

## 查询结果

**当前状态：**
- ❌ API服务当前未运行
- ❌ 没有API调用日志
- ✅ 代码已更新，支持日志记录

---

## ✅ 已添加的功能

### 1. 请求日志中间件
记录所有API请求：
- 请求方法（GET/POST）
- 请求路径
- 客户端IP
- 响应状态码
- 处理时间

### 2. 详细对话日志
记录对话过程：
- 用户消息内容
- 会话ID
- Agent调用过程
- 回复内容长度
- 处理耗时

### 3. 日志文件
- 日志文件路径：`logs/api.log`
- 自动创建logs目录
- 支持UTF-8编码

### 4. 日志查询接口
- 接口：`GET /api/logs`
- 参数：`lines`（返回行数，默认50）
- 返回最近的日志内容

---

## 🚀 如何使用日志功能

### 步骤1：启动API服务

```bash
# Windows
双击：一键启动.bat

# Mac/Linux
./一键启动.sh

# 或直接运行
python api_server.py
```

### 步骤2：查看日志

**方法1：查看日志文件**

```bash
# 查看最新的50行
tail -n 50 logs/api.log

# 实时查看日志
tail -f logs/api.log

# 查看所有日志
cat logs/api.log
```

**方法2：通过API接口查询**

访问：`http://localhost:8000/api/logs`

或使用curl：
```bash
# 查看最近50行
curl http://localhost:8000/api/logs

# 查看最近100行
curl "http://localhost:8000/api/logs?lines=100"
```

**方法3：在浏览器中查看**

访问：`http://localhost:8000/api/logs`

返回示例：
```json
{
  "status": "success",
  "total_lines": 120,
  "returned_lines": 50,
  "logs": [
    "2026-04-27 18:00:00 [INFO] 📥 请求: GET /health",
    "2026-04-27 18:00:00 [INFO] 📤 响应: 200 (0.005s)",
    "2026-04-27 18:00:05 [INFO] 📥 请求: POST /api/chat",
    "2026-04-27 18:00:05 [INFO]    来源: 127.0.0.1",
    "2026-04-27 18:00:05 [INFO] 🎯 收到对话请求: 生成今日选题清单...",
    "2026-04-27 18:00:05 [INFO]    会话ID: 新建",
    "2026-04-27 18:00:05 [INFO] 🔄 调用Agent...",
    "2026-04-27 18:00:08 [INFO] ✅ Agent回复成功 (耗时: 3.245s)",
    "2026-04-27 18:00:08 [INFO]    回复长度: 1234 字符",
    "2026-04-27 18:00:08 [INFO] 📤 响应: 200 (3.256s)"
  ]
}
```

---

## 📝 日志格式说明

### 请求日志
```
2026-04-27 18:00:00 [INFO] 📥 请求: POST /api/chat
2026-04-27 18:00:00 [INFO]    来源: 127.0.0.1
```

### 对话日志
```
2026-04-27 18:00:05 [INFO] 🎯 收到对话请求: 生成今日选题清单...
2026-04-27 18:00:05 [INFO]    会话ID: session_20260427_180005
2026-04-27 18:00:05 [INFO] 🔄 调用Agent...
2026-04-27 18:00:08 [INFO] ✅ Agent回复成功 (耗时: 3.245s)
2026-04-27 18:00:08 [INFO]    回复长度: 1234 字符
```

### 响应日志
```
2026-04-27 18:00:08 [INFO] 📤 响应: 200 (3.256s)
```

### 错误日志
```
2026-04-27 18:00:10 [ERROR] ❌ 对话处理失败: 分隔符未找到
```

---

## 📊 日志分析

### 统计API调用次数

```bash
# 统计POST请求次数
grep "POST /api/chat" logs/api.log | wc -l

# 统计健康检查次数
grep "GET /health" logs/api.log | wc -l

# 统计错误次数
grep "ERROR" logs/api.log | wc -l
```

### 查看特定时间段的日志

```bash
# 查看今天的日志
grep "2026-04-27" logs/api.log

# 查看最近1小时的日志
grep "$(date +%Y-%m-%d)" logs/api.log | tail -50
```

### 查看最慢的请求

```bash
# 提取所有响应时间，按时间排序
grep "响应:" logs/api.log | awk '{print $NF}' | sort -rn | head -10
```

---

## 🔍 如何验证API是否被调用

### 方法1：查看日志文件

```bash
# 启动服务后，查看日志
tail -f logs/api.log

# 打开网页发送消息
# 如果看到类似的日志，说明API被调用了
```

### 方法2：访问日志接口

```bash
# 访问日志接口
curl http://localhost:8000/api/logs

# 如果返回logs数组中有内容，说明API被调用过
```

### 方法3：检查日志文件是否存在

```bash
# 检查日志文件
ls -la logs/api.log

# 如果文件存在且有内容，说明API被调用过
```

---

## 💡 使用场景

### 场景1：检查同事是否在使用

```bash
# 查看今天的日志
grep "$(date +%Y-%m-%d)" logs/api.log

# 统计今天的调用次数
grep "POST /api/chat" logs/api.log | grep "$(date +%Y-%m-%d)" | wc -l
```

### 场景2：查看平均响应时间

```bash
# 提取所有响应时间
grep "响应:" logs/api.log | grep -oP '\(\d+\.\d+s\)' | sed 's/[()s]//g' | awk '{sum+=$1; count++} END {print "平均响应时间:", sum/count, "秒"}'
```

### 场景3：排查问题

```bash
# 查看所有错误
grep "ERROR" logs/api.log

# 查看超时的请求
grep -E "耗时: [5-9]\.\d+s|耗时: [1-9][0-9]\.\d+s" logs/api.log
```

---

## 📂 日志文件管理

### 日志文件位置

```
workspace/projects/
└── logs/
    ├── api.log          # API服务日志
    └── daily_push.log   # 定时推送日志
```

### 清理日志

```bash
# 清空日志文件
echo "" > logs/api.log

# 删除日志文件
rm logs/api.log

# 只保留最近1000行
tail -n 1000 logs/api.log > logs/api.log.tmp
mv logs/api.log.tmp logs/api.log
```

### 日志轮转（可选）

如果日志文件太大，可以设置自动轮转：

```bash
# 添加到crontab，每天轮转一次
0 0 * * * mv /workspace/projects/logs/api.log /workspace/projects/logs/api.log.$(date +\%Y\%m\%d)
```

---

## 🎯 快速开始

### 启动并查看日志

```bash
# 1. 启动服务
python api_server.py

# 2. 打开另一个终端，查看日志
tail -f logs/api.log

# 3. 打开网页发送消息

# 4. 查看日志输出
```

### 通过API查询日志

```bash
# 启动服务后
curl http://localhost:8000/api/logs

# 或在浏览器访问
http://localhost:8000/api/logs
```

---

## 📞 总结

**当前状态：**
- ✅ 日志功能已添加
- ✅ 代码已推送到GitHub
- ⏳ 需要重启服务才能使用

**使用步骤：**
1. 重启API服务（双击一键启动脚本）
2. 使用网页发送消息
3. 查看日志（`tail -f logs/api.log`）
4. 或访问 `http://localhost:8000/api/logs`

**现在可以追踪所有API调用了！** 🚀
