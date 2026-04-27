"""
企业微信机器人消息推送工具
支持发送文本、markdown、图片、图文、文件、语音、模板卡片等七种消息类型
"""
import re
import json
import requests
from langchain.tools import tool
from coze_workload_identity import Client
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.log.write_log import request_context
from cozeloop.decorator import observe


def _get_webhook_key() -> str:
    """
    获取企业微信机器人webhook_key

    Returns:
        webhook_key字符串

    Raises:
        ValueError: 当未配置webhook_key时抛出
    """
    client = Client()
    wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
    if not wechat_bot_credential:
        raise ValueError("企业微信机器人未配置凭证，请先完成集成配置")

    webhook_key = json.loads(wechat_bot_credential).get("webhook_key")
    if not webhook_key:
        raise ValueError("webhook_key配置缺失")

    # 如果webhook_key是完整URL，提取key部分
    if "https" in webhook_key:
        match = re.search(r"key=([a-zA-Z0-9-]+)", webhook_key)
        if match:
            webhook_key = match.group(1)

    return webhook_key


def _send_request(payload: dict) -> dict:
    """
    发送HTTP请求到企业微信webhook

    Args:
        payload: 请求体数据

    Returns:
        企业微信返回的响应数据

    Raises:
        Exception: 当请求失败时抛出
    """
    webhook_key = _get_webhook_key()
    send_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

    try:
        response = requests.post(
            send_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=15
        )
        response.raise_for_status()
        result = response.json()

        if result.get("errcode") != 0:
            raise Exception(f"发送失败: {result.get('errmsg')}")

        return result
    except requests.RequestException as e:
        raise Exception(f"网络请求异常: {str(e)}")


@tool
def send_text_to_wechat(content: str, mentioned_list: list = None, mentioned_mobile_list: list = None) -> str:
    """
    发送文本消息到企业微信群聊

    Args:
        content: 文本内容，UTF-8编码，最长不超过2048字节
        mentioned_list: @的用户userid列表，例如["user1", "@all"]
        mentioned_mobile_list: @的手机号列表，例如["13800001111", "@all"]

    Returns:
        发送结果描述

    Example:
        send_text_to_wechat(content="大家好，这是今日选题清单", mentioned_list=["@all"])
    """
    ctx = request_context.get() or new_context(method="send_text_to_wechat")

    payload = {
        "msgtype": "text",
        "text": {
            "content": content,
        }
    }

    if mentioned_list:
        payload["text"]["mentioned_list"] = mentioned_list
    if mentioned_mobile_list:
        payload["text"]["mentioned_mobile_list"] = mentioned_mobile_list

    try:
        result = _send_request(payload)
        return f"文本消息发送成功: {content[:50]}..."
    except Exception as e:
        return f"文本消息发送失败: {str(e)}"


@tool
def send_markdown_to_wechat(content: str) -> str:
    """
    发送Markdown消息到企业微信群聊

    Args:
        content: Markdown文本内容，UTF-8编码，最长不超过4096字节
                 支持标准Markdown语法

    Returns:
        发送结果描述

    Example:
        send_markdown_to_wechat(content="# 今日选题清单\\n\\n## 专题A\\n- 选题1\\n- 选题2")
    """
    ctx = request_context.get() or new_context(method="send_markdown_to_wechat")

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }

    try:
        result = _send_request(payload)
        return f"Markdown消息发送成功"
    except Exception as e:
        return f"Markdown消息发送失败: {str(e)}"


@tool
def send_news_to_wechat(title: str, description: str, url: str, picurl: str) -> str:
    """
    发送图文消息到企业微信群聊

    Args:
        title: 标题
        description: 描述
        url: 跳转链接
        picurl: 图片URL

    Returns:
        发送结果描述

    Example:
        send_news_to_wechat(
            title="嗨萌马今日选题",
            description="10个高质量选题",
            url="https://example.com",
            picurl="https://example.com/image.jpg"
        )
    """
    ctx = request_context.get() or new_context(method="send_news_to_wechat")

    payload = {
        "msgtype": "news",
        "news": {
            "articles": [{
                "title": title,
                "description": description,
                "url": url,
                "picurl": picurl
            }]
        }
    }

    try:
        result = _send_request(payload)
        return f"图文消息发送成功: {title}"
    except Exception as e:
        return f"图文消息发送失败: {str(e)}"
