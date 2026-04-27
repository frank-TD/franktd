#!/usr/bin/env python3
"""
嗨萌马每日选题定时推送脚本
支持：
- GitHub Actions定时任务
- 本地/服务器手动运行
- 定时任务（crontab）调度
"""
import os
import sys
import json
import time
import logging
from datetime import datetime
from typing import Dict, Optional

# 设置项目根目录
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'scripts'))
sys.path.insert(0, os.path.join(project_root, 'src'))  # 添加src目录到路径

# 确保日志目录存在
os.makedirs('logs', exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/daily_push.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class WeComAPIClient:
    """企业微信API客户端（HTTP模式）"""

    def __init__(self, bot_id: str, secret: str):
        self.bot_id = bot_id
        self.secret = secret
        self.access_token = None
        self.token_expires_at = 0

    def get_access_token(self) -> str:
        """获取access_token（自动缓存）"""
        # 如果token未过期，直接返回
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token

        import requests

        # 企业微信机器人获取token的端点
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"
        params = {
            "bot_id": self.bot_id,
            "secret": self.secret
        }

        try:
            # 企业微信智能机器人不需要先获取token，直接发送消息
            logger.info("使用企业微信智能机器人API，无需获取access_token")
            return None

        except Exception as e:
            logger.error(f"初始化API异常: {str(e)}")
            raise

    def send_text_message(self, content: str, chatid: Optional[str] = None) -> Dict:
        """
        发送文本消息到企业微信

        Args:
            content: 消息内容
            chatid: 群聊ID（可选），如果不指定则发送到机器人所在的所有群聊

        Returns:
            响应结果
        """
        import requests

        # 企业微信智能机器人端点
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

        data = {
            "bot_id": self.bot_id,
            "secret": self.secret,
            "msgtype": "text",
            "text": {
                "content": content
            }
        }

        # 如果指定了群聊ID，添加到请求中
        if chatid:
            data["chatid"] = chatid

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result.get("errcode") == 0:
                logger.info(f"✓ 消息发送成功")
            else:
                logger.warning(f"⚠ 消息发送失败: {result.get('errmsg')}")

            return result

        except Exception as e:
            logger.error(f"✗ 发送消息异常: {str(e)}")
            raise

    def send_markdown_message(self, content: str, chatid: Optional[str] = None) -> Dict:
        """
        发送Markdown消息到企业微信

        Args:
            content: Markdown格式的内容
            chatid: 群聊ID（可选）

        Returns:
            响应结果
        """
        import requests

        # 企业微信智能机器人端点
        url = "https://qyapi.weixin.qq.com/cgi-bin/message/send"

        data = {
            "bot_id": self.bot_id,
            "secret": self.secret,
            "msgtype": "markdown",
            "markdown": {
                "content": content
            }
        }

        if chatid:
            data["chatid"] = chatid

        try:
            response = requests.post(url, json=data, timeout=10)
            result = response.json()

            if result.get("errcode") == 0:
                logger.info(f"✓ Markdown消息发送成功")
            else:
                logger.warning(f"⚠ Markdown消息发送失败: {result.get('errmsg')}")

            return result

        except Exception as e:
            logger.error(f"✗ 发送Markdown消息异常: {str(e)}")
            raise


def generate_daily_topic() -> str:
    """
    生成每日选题清单

    Returns:
        选题内容（Markdown格式）
    """
    import sys
    from agents.agent import build_agent

    try:
        logger.info("🔄 正在初始化Agent...")
        agent = build_agent()

        logger.info("🔄 正在生成选题清单...")

        # 构造生成选题的提示词
        prompt = """请为我生成今日的短视频选题清单，包含以下两个专题：

**专题A：泛流量热点选题（5条）**
- 目标：打造泛流量爆款
- 要求：抓取抖音、微博、小红书近7天热点
- 限制：排除明星、体育赛事、商业营销、政治话题

**专题B：儿童安全教育选题（5条）**
- 目标：打造IP人设
- 要求：贴合儿童安全教育主题
- 限制：符合儿童安全、亲子互动、生活常识

**格式要求：**
请使用Markdown格式输出，包含：
- 选题标题
- 热点来源
- 创意方向
- 预估热度
- 推荐理由

请确保选题质量高，具有传播价值！"""

        # 调用Agent
        response = agent.invoke(
            {"messages": [prompt]},
            config={"configurable": {"thread_id": f"daily_push_{datetime.now().strftime('%Y%m%d')}"}}
        )

        # 提取生成的选题内容
        topic_content = response["messages"][-1].content

        logger.info("✓ 选题生成成功")
        return topic_content

    except Exception as e:
        logger.error(f"✗ 生成选题失败: {str(e)}")
        # 返回错误提示
        return f"""
⚠️ **选题生成失败**

生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

错误信息：{str(e)}

请检查：
1. Agent配置是否正确
2. 热点数据源是否可用
3. 网络连接是否正常
"""


def push_to_wecom():
    """推送选题到企业微信"""
    logger.info("=" * 60)
    logger.info("嗨萌马每日选题推送服务")
    logger.info("=" * 60)

    # 1. 获取配置
    bot_id = os.getenv("WECOM_BOT_ID", "aibylL5aVP4HUVHdyCZfVQzdEUa-FNmAwas")
    secret = os.getenv("WECOM_BOT_SECRET", "yTNzMOuXQpXBk8ldjfVne1BetWcB4O8eJu87LxvWWto")

    logger.info(f"📅 推送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"🤖 机器人ID：{bot_id[:20]}...")

    try:
        # 2. 生成选题
        logger.info("\n" + "=" * 60)
        logger.info("步骤1：生成选题清单")
        logger.info("=" * 60)

        topic_content = generate_daily_topic()

        # 3. 推送到企业微信
        logger.info("\n" + "=" * 60)
        logger.info("步骤2：推送到企业微信")
        logger.info("=" * 60)

        wecom_client = WeComAPIClient(bot_id, secret)

        # 添加标题
        final_content = f"""# 📌 嗨萌马每日选题清单

**生成时间：** {datetime.now().strftime('%Y年%m月%d日 %H:%M')}

---

{topic_content}

---

*此选题由嗨萌马短视频创作管家自动生成*
"""

        # 发送Markdown消息
        result = wecom_client.send_markdown_message(final_content)

        # 4. 结果统计
        logger.info("\n" + "=" * 60)
        logger.info("推送完成")
        logger.info("=" * 60)

        if result.get("errcode") == 0:
            logger.info(f"✅ 推送成功！")
            logger.info(f"📊 消息ID: {result.get('msgid')}")
            return True
        else:
            logger.error(f"❌ 推送失败: {result.get('errmsg')}")
            return False

    except Exception as e:
        logger.error(f"\n❌ 推送流程异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """主函数"""
    try:
        success = push_to_wecom()
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        logger.info("\n⚠ 用户中断")
        sys.exit(1)
    except Exception as e:
        logger.error(f"\n❌ 程序异常: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
