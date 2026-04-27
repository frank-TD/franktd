"""
嗨萌马Agent API服务
提供RESTful API接口，供前端调用
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
from datetime import datetime
import logging

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from agents.agent import build_agent

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/api.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# 确保日志目录存在
os.makedirs('logs', exist_ok=True)

# 初始化FastAPI应用
app = FastAPI(
    title="嗨萌马Agent API",
    description="短视频创作管家API服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有API请求"""
    start_time = datetime.now()

    # 记录请求信息
    logger.info(f"📥 请求: {request.method} {request.url.path}")
    logger.info(f"   来源: {request.client.host if request.client else 'unknown'}")

    # 处理请求
    response = await call_next(request)

    # 计算处理时间
    duration = (datetime.now() - start_time).total_seconds()

    # 记录响应信息
    logger.info(f"📤 响应: {response.status_code} ({duration:.3f}s)")

    return response

# 全局变量
agent_instance = None
agent_initialized = False

# 数据模型
class Message(BaseModel):
    role: str  # "user" 或 "assistant"
    content: str
    timestamp: str

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    timestamp: str
    session_id: str


def initialize_agent():
    """初始化Agent（单例模式）"""
    global agent_instance, agent_initialized

    if not agent_initialized:
        try:
            print("正在初始化Agent...")
            agent_instance = build_agent()
            agent_initialized = True
            print("✓ Agent初始化成功")
        except Exception as e:
            print(f"✗ Agent初始化失败: {str(e)}")
            agent_initialized = False
            raise

    return agent_instance


@app.get("/")
async def root():
    """根路径"""
    return {
        "service": "嗨萌马Agent API",
        "version": "1.0.0",
        "status": "running",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    try:
        if agent_initialized:
            return {"status": "healthy", "agent": "ready"}
        else:
            initialize_agent()
            return {"status": "healthy", "agent": "ready"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    与Agent对话

    Args:
        request: 对话请求

    Returns:
        Agent的回复
    """
    start_time = datetime.now()
    logger.info(f"🎯 收到对话请求: {request.message[:50]}...")
    logger.info(f"   会话ID: {request.session_id or '新建'}")

    try:
        # 初始化Agent
        agent = initialize_agent()

        # 生成会话ID
        session_id = request.session_id or f"session_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 调用Agent
        logger.info(f"🔄 调用Agent...")
        response = agent.invoke(
            {"messages": [request.message]},
            config={"configurable": {"thread_id": session_id}}
        )

        # 提取回复内容
        assistant_message = response["messages"][-1].content

        # 计算处理时间
        duration = (datetime.now() - start_time).total_seconds()

        logger.info(f"✅ Agent回复成功 (耗时: {duration:.3f}s)")
        logger.info(f"   回复长度: {len(assistant_message)} 字符")

        return ChatResponse(
            message=assistant_message,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            session_id=session_id
        )

    except Exception as e:
        logger.error(f"❌ 对话处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")


@app.get("/api/info")
async def get_info():
    """获取API信息"""
    return {
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
            "GET /health": "健康检查",
            "GET /api/logs": "查看API日志"
        }
    }


@app.get("/api/logs")
async def get_logs(lines: int = 50):
    """
    查看API日志

    Args:
        lines: 返回的日志行数

    Returns:
        最近的日志内容
    """
    try:
        log_file = os.path.join(os.path.dirname(__file__), 'logs', 'api.log')

        if not os.path.exists(log_file):
            return {
                "status": "no_logs",
                "message": "暂无日志文件"
            }

        # 读取最后N行日志
        with open(log_file, 'r', encoding='utf-8') as f:
            all_lines = f.readlines()
            recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines

        return {
            "status": "success",
            "total_lines": len(all_lines),
            "returned_lines": len(recent_lines),
            "logs": [line.strip() for line in recent_lines]
        }

    except Exception as e:
        logger.error(f"读取日志失败: {str(e)}")
        return {
            "status": "error",
            "message": f"读取日志失败: {str(e)}"
        }


if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("嗨萌马Agent API服务")
    print("=" * 60)
    print()

    # 初始化Agent
    initialize_agent()

    # 启动服务
    print()
    print("🚀 启动API服务...")
    print("📱 访问地址：http://localhost:8000")
    print("📚 API文档：http://localhost:8000/docs")
    print()
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8000)
