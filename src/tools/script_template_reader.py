"""
脚本模板读取工具 - 用于参考标准脚本格式
"""
from langchain.tools import tool
import os


@tool
def get_script_template() -> str:
    """
    读取嗨萌马标准脚本模板，用于参考脚本格式和结构

    Returns:
        返回标准脚本模板的完整内容，包括六大类脚本的详细格式示例
    """
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    template_path = os.path.join(workspace_path, "assets/script_template.txt")

    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return f"""
================================================================================
嗨萌马标准脚本模板
================================================================================

{content}

================================================================================
使用说明：
1. 参考模板中的六大类脚本格式：情绪管理类、社交与校园关系类、亲子沟通与家庭类、学习与习惯培养类、专注力与屏幕管理类、高共鸣"反转"类
2. 每个脚本包含：原始标题、优化标题、核心洞察、详细的视频脚本（分镜、画面描述、文案/旁白、时长）
3. 生成新脚本时，请严格遵循此格式和结构
================================================================================
"""
    except FileNotFoundError:
        return "错误：未找到脚本模板文件（assets/script_template.txt），请检查文件是否存在。"
    except Exception as e:
        return f"读取脚本模板时出错：{str(e)}"
