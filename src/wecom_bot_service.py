"""
企业微信机器人监听服务
持续监听企业微信消息并转发给Agent处理
"""
import json
import asyncio
import os
import websockets
from typing import Optional
from src.agents.agent import build_agent, AgentState
from langchain_core.messages import HumanMessage, AIMessage


class WeComBotService:
    """企业微信机器人服务"""
    
    def __init__(self, bot_id: str, secret: str):
        self.bot_id = bot_id
        self.secret = secret
        self.ws_url = "wss://openws.work.weixin.qq.com"
        self.websocket: Optional = None
        self.is_connected = False
        self.agent = None
        
    async def connect(self):
        """建立WebSocket长连接"""
        try:
            print(f"[企微机器人] 正在连接企业微信...")
            
            self.websocket = await websockets.connect(
                self.ws_url,
                ping_interval=30,
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
            print("[企微机器人] ✓ 订阅指令已发送")
            
            # 等待订阅结果
            response = await asyncio.wait_for(self.websocket.recv(), timeout=10)
            result = json.loads(response)
            
            if result.get("errcode") == 0:
                self.is_connected = True
                print("[企微机器人] ✅ 连接成功！")
                
                # 初始化Agent
                print("[企微机器人] 正在初始化Agent...")
                self.agent = build_agent()
                print("[企微机器人] ✅ Agent初始化完成")
                
                return True
            else:
                error_msg = result.get("errmsg", "未知错误")
                print(f"[企微机器人] ❌ 订阅失败: {error_msg}")
                return False
                
        except asyncio.TimeoutError:
            print("[企微机器人] ❌ 连接超时")
            return False
        except Exception as e:
            print(f"[企微机器人] ❌ 连接失败: {str(e)}")
            return False
    
    async def send_message(self, content: str, msg_type: str = "text"):
        """发送消息"""
        if not self.is_connected:
            print("[企微机器人] 未连接，无法发送消息")
            return
        
        msg = {
            "msgtype": msg_type,
            msg_type: {
                "content": content
            }
        }
        
        await self.websocket.send(json.dumps(msg))
        print(f"[企微机器人] ✓ 消息已发送: {content[:50]}...")
    
    async def handle_message(self, message_data: dict):
        """处理收到的消息"""
        try:
            print(f"[企微机器人] 收到消息: {message_data}")
            
            # 解析消息内容
            msg_type = message_data.get("msgtype", "")
            user_id = message_data.get("userid", "")
            
            if msg_type == "text":
                content = message_data.get("text", {}).get("content", "")
                print(f"[企微机器人] 用户消息: {content}")
                
                # 转发给Agent处理
                if self.agent:
                    print("[企微机器人] 正在调用Agent处理...")
                    
                    # 创建会话状态
                    config = {"configurable": {"thread_id": user_id or "default"}}
                    
                    # 调用Agent
                    response = await self.agent.ainvoke(
                        {"messages": [HumanMessage(content=content)]},
                        config=config
                    )
                    
                    # 获取回复
                    if response and "messages" in response:
                        last_message = response["messages"][-1]
                        reply_content = last_message.content
                        
                        print(f"[企微机器人] Agent回复: {reply_content[:100]}...")
                        
                        # 发送回复
                        await self.send_message(reply_content)
                    else:
                        await self.send_message("抱歉，我无法处理您的请求。")
                else:
                    await self.send_message("Agent未初始化，请稍后重试。")
            
        except Exception as e:
            print(f"[企微机器人] 处理消息错误: {str(e)}")
            import traceback
            traceback.print_exc()
    
    async def listen_messages(self):
        """持续监听消息"""
        if not self.is_connected:
            print("[企微机器人] 未连接，无法监听消息")
            return
        
        print("[企微机器人] 开始监听消息...")
        
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    
                    # 处理消息
                    await self.handle_message(data)
                    
                except Exception as e:
                    print(f"[企微机器人] 处理单条消息错误: {str(e)}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("[企微机器人] 连接已关闭")
            self.is_connected = False
        except Exception as e:
            print(f"[企微机器人] 监听错误: {str(e)}")
            self.is_connected = False
    
    async def close(self):
        """关闭连接"""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            print("[企微机器人] 连接已关闭")


async def main():
    """主函数"""
    # 从环境变量获取凭证
    bot_id = os.getenv("WECOM_BOT_ID", "aibylL5aVP4HUVHdyCZfVQzdEUa-FNmAwas")
    secret = os.getenv("WECOM_BOT_SECRET", "yTNzMOuXQpXBk8ldjfVne1BetWcB4O8eJu87LxvWWto")
    
    # 创建服务
    service = WeComBotService(bot_id, secret)
    
    # 连接
    if not await service.connect():
        print("[企微机器人] 连接失败，退出")
        return
    
    # 开始监听
    await service.listen_messages()


if __name__ == "__main__":
    print("[企微机器人] 启动服务...")
    asyncio.run(main())
