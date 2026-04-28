"""
选题历史记录管理工具
用于记录和查询已生成的选题，防止重复
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from langchain.tools import tool

# 历史记录文件路径
HISTORY_FILE = os.path.join(os.path.dirname(__file__), '../../assets/topic_history.json')


def _ensure_history_file():
    """确保历史记录文件存在"""
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump({"topics": [], "last_updated": datetime.now().isoformat()}, f, ensure_ascii=False)


def _load_history() -> Dict:
    """加载历史记录"""
    _ensure_history_file()
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"topics": [], "last_updated": datetime.now().isoformat()}


def _save_history(history: Dict):
    """保存历史记录"""
    _ensure_history_file()
    history["last_updated"] = datetime.now().isoformat()
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)


@tool
def get_recent_topics(days: int = 7) -> str:
    """
    获取最近N天内已生成的选题列表

    Args:
        days: 查询最近多少天的选题（默认7天）

    Returns:
        最近生成的选题标题列表
    """
    try:
        history = _load_history()
        topics = history.get("topics", [])

        # 计算截止日期
        cutoff_date = datetime.now() - timedelta(days=days)

        # 筛选最近N天的选题
        recent_topics = []
        for topic in topics:
            topic_date = datetime.fromisoformat(topic.get("date", "2000-01-01"))
            if topic_date >= cutoff_date:
                recent_topics.append(topic)

        if not recent_topics:
            return "最近{}天内没有生成过选题。".format(days)

        # 格式化输出
        output = [f"最近{days}天内已生成的选题（共{len(recent_topics)}个）：\n"]
        for i, topic in enumerate(recent_topics, 1):
            output.append(f"{i}. {topic.get('title', '未知标题')} ({topic.get('date', '未知日期')[:10]})")
            if topic.get('category'):
                output.append(f"   分类：{topic['category']}")

        return "\n".join(output)

    except Exception as e:
        return f"查询历史选题时出错：{str(e)}"


@tool
def check_topic_duplicate(topic_title: str) -> str:
    """
    检查某个选题是否在最近7天内已经生成过

    Args:
        topic_title: 要检查的选题标题

    Returns:
        检查结果：是否重复，以及相似的历史选题
    """
    try:
        history = _load_history()
        topics = history.get("topics", [])

        # 计算7天前的日期
        cutoff_date = datetime.now() - timedelta(days=7)

        # 检查是否有相似或相同的选题
        duplicates = []
        for topic in topics:
            topic_date = datetime.fromisoformat(topic.get("date", "2000-01-01"))
            if topic_date >= cutoff_date:
                # 简单匹配：标题包含关系或相似度
                existing_title = topic.get('title', '')
                if (topic_title in existing_title or
                    existing_title in topic_title or
                    _similarity_check(topic_title, existing_title)):
                    duplicates.append({
                        "title": existing_title,
                        "date": topic.get("date", "")[:10],
                        "similarity": "高"
                    })

        if duplicates:
            output = [f"⚠️ 检测到重复或相似选题！\n"]
            output.append(f"当前选题：{topic_title}\n")
            output.append("相似的历史选题：")
            for dup in duplicates:
                output.append(f"  • {dup['title']} ({dup['date']}) [相似度：{dup['similarity']}]")
            return "\n".join(output)
        else:
            return f"✅ 选题\"{topic_title}\"未发现重复，可以生成。"

    except Exception as e:
        return f"检查重复时出错：{str(e)}"


@tool
def record_generated_topic(title: str, category: str = "", platform: str = "") -> str:
    """
    记录已生成的选题到历史记录中

    Args:
        title: 选题标题
        category: 选题分类（如"泛流量热点"、"儿童安全教育"）
        platform: 来源平台（如"抖音"、"微博"、"小红书"）

    Returns:
        记录结果
    """
    try:
        history = _load_history()

        # 添加新选题
        new_topic = {
            "title": title,
            "category": category,
            "platform": platform,
            "date": datetime.now().isoformat(),
            "id": f"topic_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        }

        history["topics"].append(new_topic)

        # 只保留最近30天的记录（防止文件过大）
        cutoff_date = datetime.now() - timedelta(days=30)
        history["topics"] = [
            t for t in history["topics"]
            if datetime.fromisoformat(t.get("date", "2000-01-01")) >= cutoff_date
        ]

        _save_history(history)

        return f"✅ 已记录选题：{title}"

    except Exception as e:
        return f"记录选题时出错：{str(e)}"


def _similarity_check(title1: str, title2: str) -> bool:
    """
    简单的相似度检查

    Args:
        title1: 第一个标题
        title2: 第二个标题

    Returns:
        是否相似
    """
    # 提取关键词（简单的分词）
    def extract_keywords(text):
        # 移除常见停用词
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        words = set(text.lower()) - stop_words
        return words

    keywords1 = extract_keywords(title1)
    keywords2 = extract_keywords(title2)

    # 计算Jaccard相似度
    if not keywords1 or not keywords2:
        return False

    intersection = len(keywords1 & keywords2)
    union = len(keywords1 | keywords2)

    similarity = intersection / union if union > 0 else 0

    # 相似度超过0.5认为是相似的
    return similarity > 0.5


# 非工具函数，供Agent内部使用
def get_all_topic_titles(days: int = 7) -> List[str]:
    """
    获取最近N天所有选题标题（供Agent内部使用）

    Args:
        days: 查询天数

    Returns:
        选题标题列表
    """
    try:
        history = _load_history()
        topics = history.get("topics", [])

        cutoff_date = datetime.now() - timedelta(days=days)

        titles = []
        for topic in topics:
            topic_date = datetime.fromisoformat(topic.get("date", "2000-01-01"))
            if topic_date >= cutoff_date:
                titles.append(topic.get('title', ''))

        return titles
    except Exception:
        return []
