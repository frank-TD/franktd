"""
热点筛选工具 - 支持白名单和黑名单过滤
"""
from typing import List, Dict
import re
from langchain.tools import tool


def _filter_hot_topics_by_keywords(hot_topics_text: str, whitelist: List[str], blacklist: List[str]) -> str:
    """
    根据白名单和黑名单过滤热点（内部实现函数）

    Args:
        hot_topics_text: 热点文本内容
        whitelist: 白名单关键词列表
        blacklist: 黑名单关键词列表

    Returns:
        过滤后的热点文本
    """
    # 配置白名单和黑名单
    default_whitelist = [
        "生活", "职场", "热梗", "治愈", "趣味",
        "生活技巧", "职场技巧", "搞笑", "萌宠", "美食",
        "旅游", "穿搭", "健身", "读书", "成长",
        "正能量", "励志", "温暖", "情感", "亲子",
        "育儿", "家庭", "健康", "知识", "科普",
        "娱乐", "电影", "音乐", "游戏", "运动"
    ]

    default_blacklist = [
        "时政", "政治", "选举", "政策", "法律诉讼",
        "负面", "丑闻", "犯罪", "暴力", "恐怖",
        "低俗", "色情", "裸露", "成人",
        "敏感", "争议", "歧视", "仇恨",
        "死亡", "事故", "灾难", "战争",
        "疫情", "病毒", "疾病传播",
        "赌博", "诈骗", "违法"
    ]

    # 使用传入的列表，如果没有则使用默认值
    whitelist = whitelist if whitelist else default_whitelist
    blacklist = blacklist if blacklist else default_blacklist

    # 按平台分割热点文本
    lines = hot_topics_text.split('\n')
    filtered_lines = []
    current_topic_lines = []
    include_topic = False
    in_topic = False

    for line in lines:
        # 检测是否是新的热点条目
        if line.startswith('【热点') or line.startswith('| 热点标题'):
            # 如果之前有正在处理的热点，先处理它
            if current_topic_lines and include_topic:
                filtered_lines.extend(current_topic_lines)
            # 开始新的热点
            current_topic_lines = [line]
            in_topic = True
            include_topic = False
        elif in_topic:
            current_topic_lines.append(line)
            # 检查是否到达热点结尾（空行或分隔线）
            if line.strip() == '' or line.startswith('---') or line.startswith('='):
                # 对整个热点进行关键词检查
                topic_text = ' '.join(current_topic_lines)

                # 检查黑名单
                blacklist_match = False
                for keyword in blacklist:
                    if keyword in topic_text:
                        blacklist_match = True
                        break

                # 检查白名单
                whitelist_match = False
                for keyword in whitelist:
                    if keyword in topic_text:
                        whitelist_match = True
                        break

                # 决定是否保留：不在黑名单且在白名单
                if not blacklist_match and whitelist_match:
                    include_topic = True

                # 清空当前热点
                current_topic_lines = []
                in_topic = False
        else:
            # 保留非热点内容（如标题、分隔线等）
            filtered_lines.append(line)

    # 处理最后一个热点
    if current_topic_lines and include_topic:
        filtered_lines.extend(current_topic_lines)

    # 如果所有内容都被过滤掉了，返回提示信息
    if not filtered_lines or all(line.strip() == '' for line in filtered_lines):
        return "未找到符合筛选条件的热点，请调整筛选条件或稍后再试。"

    return '\n'.join(filtered_lines)


@tool
def filter_hot_topics(hot_topics: str, whitelist_keywords: str = "", blacklist_keywords: str = "") -> str:
    """
    根据白名单和黑名单关键词过滤热点

    Args:
        hot_topics: 原始热点文本内容
        whitelist_keywords: 白名单关键词，多个关键词用逗号分隔（如：生活,职场,治愈）
        blacklist_keywords: 黑名单关键词，多个关键词用逗号分隔（如：时政,负面,敏感）

    Returns:
        过滤后的热点文本

    默认白名单：生活、职场、热梗、治愈、趣味、生活技巧、职场技巧、搞笑、萌宠、美食、旅游、穿搭、健身、读书、成长、正能量、励志、温暖、情感、亲子、育儿、家庭、健康、知识、科普、娱乐、电影、音乐、游戏、运动

    默认黑名单：时政、政治、选举、政策、法律诉讼、负面、丑闻、犯罪、暴力、恐怖、低俗、色情、裸露、成人、敏感、争议、歧视、仇恨、死亡、事故、灾难、战争、疫情、病毒、疾病传播、赌博、诈骗、违法
    """
    # 解析自定义白名单
    whitelist = []
    if whitelist_keywords:
        whitelist = [kw.strip() for kw in whitelist_keywords.split(',') if kw.strip()]

    # 解析自定义黑名单
    blacklist = []
    if blacklist_keywords:
        blacklist = [kw.strip() for kw in blacklist_keywords.split(',') if kw.strip()]

    # 调用内部函数进行过滤
    return _filter_hot_topics_by_keywords(hot_topics, whitelist, blacklist)


@tool
def get_filter_keywords() -> str:
    """
    获取当前配置的白名单和黑名单关键词

    Returns:
        返回当前的白名单和黑名单配置
    """
    default_whitelist = [
        "生活", "职场", "热梗", "治愈", "趣味",
        "生活技巧", "职场技巧", "搞笑", "萌宠", "美食",
        "旅游", "穿搭", "健身", "读书", "成长",
        "正能量", "励志", "温暖", "情感", "亲子",
        "育儿", "家庭", "健康", "知识", "科普",
        "娱乐", "电影", "音乐", "游戏", "运动"
    ]

    default_blacklist = [
        "时政", "政治", "选举", "政策", "法律诉讼",
        "负面", "丑闻", "犯罪", "暴力", "恐怖",
        "低俗", "色情", "裸露", "成人",
        "敏感", "争议", "歧视", "仇恨",
        "死亡", "事故", "灾难", "战争",
        "疫情", "病毒", "疾病传播",
        "赌博", "诈骗", "违法"
    ]

    return f"""
================================================================================
热点筛选关键词配置
================================================================================

【白名单关键词】（必须包含至少一个）
{', '.join(default_whitelist)}

【黑名单关键词】（不能包含任何）
{', '.join(default_blacklist)}

================================================================================
使用说明：
1. 热点必须包含至少一个白名单关键词才会被保留
2. 热点如果包含任何黑名单关键词，会被直接过滤
3. 可以通过 filter_hot_topics 工具自定义关键词
4. 默认配置已优化，适合短视频创作场景
================================================================================
"""
