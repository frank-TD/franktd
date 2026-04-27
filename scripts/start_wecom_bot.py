#!/usr/bin/env python3
"""
启动企业微信机器人服务
持续监听企业微信消息并自动回复
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.chdir(project_root)

print(f"项目根目录: {project_root}")
print(f"Python路径: {sys.path[:3]}")

from src.wecom_bot_service import main


if __name__ == "__main__":
    print("=" * 60)
    print("嗨萌马企业微信机器人服务")
    print("=" * 60)
    print()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[企微机器人] 服务已停止（用户中断）")
    except Exception as e:
        print(f"\n[企微机器人] 服务异常: {str(e)}")
        import traceback
        traceback.print_exc()
