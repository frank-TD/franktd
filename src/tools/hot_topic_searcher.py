"""
热点搜索工具 - 支持抖音、微博、小红书近 7 天热点搜索
"""
from langchain.tools import tool
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context


def _search_hot_topics_impl(platform: str) -> str:
    """
    搜索指定平台的近 7 天泛流量热点信息（内部实现函数）

    Args:
        platform: 平台名称，可选值：douyin（抖音）、weibo（微博）、xiaohongshu（小红书）

    Returns:
        返回该平台近 7 天的热点信息，包括标题、链接、摘要、发布时间等
    """
    ctx = new_context(method="search_hot_topics")
    client = SearchClient(ctx=ctx)

    # 根据平台构建搜索关键词
    platform_keywords = {
        "douyin": ["抖音 热门", "抖音 热点", "douyin trending", "抖音 流行"],
        "weibo": ["微博 热搜", "微博 热点", "weibo trending", "微博 流行"],
        "xiaohongshu": ["小红书 热门", "小红书 热点", "小红书 流行", "xiaohongshu hot"]
    }

    if platform not in platform_keywords:
        return f"错误：不支持的平台 '{platform}'，请选择：douyin、weibo 或 xiaohongshu"

    keywords = platform_keywords[platform]
    results = []

    # 搜索多个关键词以获取更全面的热点信息
    for keyword in keywords[:2]:  # 只搜索前2个关键词，减少数据量
        try:
            response = client.search(
                query=keyword,
                search_type="web",
                count=5,  # 减少到5条
                time_range="1w",  # 最近 7 天
                need_summary=True,
                need_url=True
            )

            if response.web_items:
                for item in response.web_items:
                    results.append({
                        "platform": platform,
                        "title": item.title,
                        "url": item.url,
                        "snippet": item.snippet,
                        "summary": item.summary,
                        "publish_time": item.publish_time,
                        "site_name": item.site_name,
                        "auth_info": item.auth_info_des
                    })
        except Exception as e:
            # 记录错误但继续搜索其他关键词
            continue

    if not results:
        return f"未找到 {platform} 平台近 7 天的热点信息，请稍后再试"

    # 格式化输出结果
    output = [f"\n{'='*80}"]
    output.append(f"📱 {platform.upper()} 平台近 7 天热点信息")
    output.append(f"{'='*80}\n")

    # 限制返回数量，避免数据过大
    for i, item in enumerate(results[:5], 1):  # 改为最多返回 5 条热点
        output.append(f"【热点 {i}】")
        output.append(f"📌 标题：{item['title']}")
        # 不输出链接，减少数据量
        if item['publish_time']:
            output.append(f"⏰ 时间：{item['publish_time']}")
        if item['site_name']:
            output.append(f"📄 来源：{item['site_name']}")
        # 截断过长的摘要
        if item['summary']:
            summary = item['summary'][:200] + "..." if len(item['summary']) > 200 else item['summary']
            output.append(f"📝 摘要：{summary}")
        elif item['snippet']:
            snippet = item['snippet'][:200] + "..." if len(item['snippet']) > 200 else item['snippet']
            output.append(f"📝 摘要：{snippet}")
        output.append("")

    return "\n".join(output)


@tool
def search_hot_topics(platform: str) -> str:
    """
    搜索指定平台的近 7 天泛流量热点信息

    Args:
        platform: 平台名称，可选值：douyin（抖音）、weibo（微博）、xiaohongshu（小红书）

    Returns:
        返回该平台近 7 天的热点信息，包括标题、链接、摘要、发布时间等
    """
    return _search_hot_topics_impl(platform)


@tool
def search_all_platforms_hot_topics() -> str:
    """
    搜索所有平台（抖音、微博、小红书）近 7 天的泛流量热点信息

    Returns:
        返回三大平台近 7 天的热点信息汇总
    """
    platforms = ["douyin", "weibo", "xiaohongshu"]
    all_results = []

    for platform in platforms:
        try:
            result = _search_hot_topics_impl(platform)
            all_results.append(result)
        except Exception as e:
            error_msg = f"搜索 {platform} 平台热点时出错：{str(e)}"
            all_results.append(error_msg)
            continue  # 即使出错也继续搜索其他平台

    # 如果所有平台都失败，返回友好的错误信息
    if all("出错" in result for result in all_results):
        return "抱歉，当前无法获取热点信息，请稍后再试。"

    return "\n\n".join(all_results)
