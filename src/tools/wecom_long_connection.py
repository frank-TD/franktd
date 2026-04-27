"""
企业微信智能机器人长连接工具
支持WebSocket双向通信，流式输出
"""
import json
import os
import asyncio
import websockets
from typing import Optional
from langchain.tools import tool
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.log.write_log import request_context


class WeComBotClient:
    """企业微信机器人长连接客户端"""
    
    def __init__(self, bot_id: str, secret: str):
        self.bot_id = bot_id
        self.secret = secret
        self.ws_url = "wss://openws.work.weixin.qq.com"  # 正确的企业微信长连接地址
        self.websocket: Optional = None
        self.is_connected = False
        
    async def connect(self):
        """建立WebSocket长连接"""
        try:
            print(f"正在连接企业微信机器人...")
            
            self.websocket = await websockets.connect(
                self.ws_url,
                ping_interval=30,  # 每30秒发送心跳
                ping_timeout=10,
                close_timeout=10
            )
            
            # 发送订阅指令
            subscribe_msg = {
                "aibot_subscribe": {
                    "bot_id": self.bot_id,
                    "secret": self.secret
                }
            }
            
            await self.websocket.send(json.dumps(subscribe_msg))
            print("✓ 订阅指令已发送")
            
            # 等待订阅结果
            response = await asyncio.wait_for(self.websocket.recv(), timeout=10)
            result = json.loads(response)
            
            if result.get("errcode") == 0:
                self.is_connected = True
                print("✅ 企业微信机器人连接成功！")
                return True
            else:
                error_msg = result.get("errmsg", "未知错误")
                raise Exception(f"订阅失败: {error_msg}")
                
        except asyncio.TimeoutError:
            raise Exception("连接超时，请检查网络或Bot ID/Secret是否正确")
        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            raise
    
    async def send_text(self, content: str, user_id: str = ""):
        """发送文本消息"""
        if not self.is_connected:
            raise Exception("未连接到企业微信，请先调用connect()")
        
        # 构造消息体
        msg = {
            "msgtype": "text",
            "text": {
                "content": content
            }
        }
        
        # 如果指定了user_id，添加到消息中
        if user_id:
            msg["text"]["mentioned_list"] = [user_id]
        
        await self.websocket.send(json.dumps(msg))
        return f"消息已发送: {content[:50]}..."
    
    async def send_markdown(self, content: str):
        """发送Markdown消息"""
        if not self.is_connected:
            raise Exception("未连接到企业微信，请先调用connect()")
        
        msg = {
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }
        
        await self.websocket.send(json.dumps(msg))
        return "Markdown消息已发送"
    
    async def close(self):
        """关闭连接"""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            print("连接已关闭")


# 全局连接实例
_bot_client: Optional[WeComBotClient] = None


def _get_bot_client() -> WeComBotClient:
    """获取机器人客户端实例"""
    global _bot_client
    
    if _bot_client is None:
        # 从环境变量读取Bot ID和Secret
        bot_id = os.getenv("WECOM_BOT_ID", "aibylL5aVP4HUVHdyCZfVQzdEUa-FNmAwas")
        secret = os.getenv("WECOM_BOT_SECRET", "yTNzMOuXQpXBk8ldjfVne1BetWcB4O8eJu87LxvWWto")
        
        if not bot_id or not secret:
            raise ValueError(
                "未配置企业微信机器人凭证！\n"
                "请设置环境变量:\n"
                "  WECOM_BOT_ID: 企业微信机器人的Bot ID\n"
                "  WECOM_BOT_SECRET: 企业微信机器人的Secret"
            )
        
        _bot_client = WeComBotClient(bot_id, secret)
    
    return _bot_client


async def _ensure_connected():
    """确保已建立连接"""
    client = _get_bot_client()
    if not client.is_connected:
        await client.connect()


@tool
def send_to_wecom_text(content: str) -> str:
    """
    发送文本消息到企业微信机器人
    
    Args:
        content: 消息内容，最长2048字节
    
    Returns:
        发送结果描述
    
    Example:
        send_to_wecom_text(content="大家好，这是今日选题清单")
    """
    ctx = request_context.get() or new_context(method="send_to_wecom_text")
    
    try:
        # 创建事件循环并运行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def send():
            await _ensure_connected()
            client = _get_bot_client()
            result = await client.send_text(content)
            return result
        
        result = loop.run_until_complete(send())
        loop.close()
        
        return f"✅ {result}"
        
    except Exception as e:
        return f"❌ 发送失败: {str(e)}"


@tool
def send_to_wecom_markdown(content: str) -> str:
    """
    发送Markdown消息到企业微信机器人（推荐用于选题清单）
    
    Args:
        content: Markdown格式内容，最长4096字节
    
    Returns:
        发送结果描述
    
    Example:
        send_to_wecom_markdown(content="# 今日选题\\n\\n- 选题1\\n- 选题2")
    """
    ctx = request_context.get() or new_context(method="send_to_wecom_markdown")
    
    try:
        # 创建事件循环并运行
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def send():
            await _ensure_connected()
            client = _get_bot_client()
            result = await client.send_markdown(content)
            return result
        
        result = loop.run_until_complete(send())
        loop.close()
        
        return f"✅ {result}"
        
    except Exception as e:
        return f"❌ 发送失败: {str(e)}"


@tool
def test_wecom_connection() -> str:
    """
    测试企业微信机器人连接状态
    
    Returns:
        连接状态描述
    """
    ctx = request_context.get() or new_context(method="test_wecom_connection")
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def test():
            client = _get_bot_client()
            if not client.is_connected:
                await client.connect()
            
            if client.is_connected:
                # 发送测试消息
                await client.send_text("🤖 嗨萌马机器人已上线，随时为您服务！")
                return "✅ 企业微信机器人连接成功！"
            else:
                return "❌ 企业微信机器人连接失败"
        
        result = loop.run_until_complete(test())
        loop.close()
        
        return result
        
    except Exception as e:
        return f"❌ 测试失败: {str(e)}"
