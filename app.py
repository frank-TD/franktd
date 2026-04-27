#!/usr/bin/env python3
"""
嗨萌马短视频创作管家 - Web对话界面
使用Streamlit构建的对话界面，支持多人同时使用
"""
import os
import sys
import json
from datetime import datetime
from typing import Dict, List

# 添加项目路径
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'src'))

import streamlit as st
from agents.agent import build_agent

# 页面配置
st.set_page_config(
    page_title="嗨萌马短视频创作管家",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease-in;
    }
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    .assistant-message {
        background: #f0f2f6;
        color: #333;
        margin-right: 2rem;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .quick-btn {
        background: #667eea;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.25rem;
        cursor: pointer;
    }
    .quick-btn:hover {
        background: #764ba2;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """初始化会话状态"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "agent" not in st.session_state:
        try:
            st.session_state.agent = build_agent()
            st.session_state.agent_loaded = True
        except Exception as e:
            st.session_state.agent_loaded = False
            st.session_state.agent_error = str(e)


def render_header():
    """渲染页面标题"""
    st.markdown("""
    <div class="main-header">
        <h1>🎬 嗨萌马短视频创作管家</h1>
        <p style="margin-top: 1rem; font-size: 1.1rem;">智能选题 · 热点捕捉 · 创意生成</p>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """渲染侧边栏"""
    with st.sidebar:
        st.header("⚙️ 设置")

        # 使用说明
        st.subheader("📖 使用说明")
        st.markdown("""
        1. 在输入框输入您的问题或需求
        2. 点击发送或按Enter键
        3. 等待Agent回复
        4. 查看对话历史

        **常用功能：**
        - 生成今日选题清单
        - 搜索热点话题
        - 分析视频创意
        - 优化选题方向
        """)

        # 快捷问题
        st.subheader("⚡ 快捷问题")
        quick_questions = [
            "生成今日选题清单",
            "搜索抖音热门话题",
            "分析儿童安全教育方向",
            "优化这个选题",
            "推荐泛流量爆款选题"
        ]

        for question in quick_questions:
            if st.button(question, key=f"quick_{question}", use_container_width=True):
                st.session_state.input_text = question
                st.rerun()

        # 对话历史
        st.subheader("💬 对话历史")
        if st.button("清空对话历史", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

        # 统计信息
        st.subheader("📊 统计信息")
        message_count = len(st.session_state.messages)
        st.metric("消息数量", message_count)

        # 技术支持
        st.subheader("📞 技术支持")
        st.markdown("""
        如有问题，请联系：
        - 技术支持：xxx
        - 项目文档：查看README.md
        """)


def render_chat():
    """渲染聊天界面"""
    # 显示历史消息
    for message in st.session_state.messages:
        with st.container():
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 用户：</strong>
                    <div style="margin-top: 0.5rem;">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message">
                    <strong>🤖 嗨萌马：</strong>
                    <div style="margin-top: 0.5rem;">{message["content"]}</div>
                </div>
                """, unsafe_allow_html=True)

    # 用户输入
    st.divider()

    # 如果有快捷问题，自动填充
    if "input_text" in st.session_state:
        default_text = st.session_state.input_text
        del st.session_state.input_text
    else:
        default_text = ""

    user_input = st.text_input(
        "💭 输入您的问题或需求...",
        value=default_text,
        placeholder="例如：生成今日选题清单",
        key="user_input"
    )

    col1, col2, col3 = st.columns([1, 1, 4])

    with col1:
        if st.button("发送", type="primary", use_container_width=True):
            if user_input:
                handle_user_message(user_input)

    with col2:
        if st.button("清空", type="secondary", use_container_width=True):
            st.session_state.messages = []
            st.rerun()


def handle_user_message(user_input: str):
    """处理用户消息"""
    # 显示用户消息
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    # 显示加载状态
    with st.spinner("🤔 嗨萌马正在思考..."):
        try:
            # 调用Agent
            response = st.session_state.agent.invoke(
                {"messages": [user_input]},
                config={"configurable": {"thread_id": f"web_{datetime.now().strftime('%Y%m%d%H%M%S')}"}}
            )

            # 提取回复内容
            assistant_response = response["messages"][-1].content

            # 显示助手消息
            st.session_state.messages.append({
                "role": "assistant",
                "content": assistant_response,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

            # 刷新页面
            st.rerun()

        except Exception as e:
            error_msg = f"❌ 处理失败：{str(e)}"
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_msg,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            st.rerun()


def render_agent_status():
    """渲染Agent状态"""
    if not st.session_state.get("agent_loaded", False):
        st.error(f"""
        ❌ Agent加载失败

        **错误信息：** {st.session_state.get("agent_error", "未知错误")}

        **可能原因：**
        1. 配置文件未正确设置
        2. API密钥未配置
        3. 依赖包未安装

        **解决方案：**
        1. 检查 `config/agent_llm_config.json`
        2. 配置环境变量
        3. 运行 `pip install -r requirements.txt`
        """)
        return False

    st.success("✅ Agent已就绪，可以开始对话！")
    return True


def main():
    """主函数"""
    # 初始化会话状态
    initialize_session_state()

    # 渲染页面标题
    render_header()

    # 渲染侧边栏
    render_sidebar()

    # 渲染Agent状态
    if not render_agent_status():
        st.stop()

    # 渲染聊天界面
    render_chat()

    # 页脚
    st.divider()
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🎬 嗨萌马短视频创作管家 | 基于LangChain构建</p>
        <p>💡 提示：输入您的问题或需求，嗨萌马将为您提供专业的选题建议</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
