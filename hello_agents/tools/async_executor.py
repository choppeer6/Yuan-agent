import asyncio
import re
from typing import List, Dict, Any, Optional
from .registry import ToolRegistry
from ..core.exceptions import ToolError, ToolNotFoundError

class AsyncExecutor:
    """
    异步工具执行器。
    支持从文本中解析多个 Action 并并发执行。
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    async def execute_all(self, text: str) -> Optional[str]:
        """
        解析并并发执行所有匹配到的 Action。
        返回合并后的 Observation 字符串。
        """
        # 1. 提取所有 Action
        # 匹配格式: Action: tool_name("arguments")
        actions = re.findall(r'Action:\s*(\w+)\((.*)\)', text)
        if not actions:
            return None

        print(f"⚡ [Async] 发现 {len(actions)} 个并发任务，准备执行...")

        # 2. 封装成异步任务
        tasks = []
        for tool_name, args_str in actions:
            clean_args = args_str.strip().strip('"').strip("'")
            tasks.append(self._run_tool_async(tool_name, clean_args))

        # 3. 并发执行并等待结果
        results = await asyncio.gather(*tasks)

        # 4. 合并结果
        observation_list = []
        for (tool_name, _), result in zip(actions, results):
            observation_list.append(f"Observation [{tool_name}]: {result}")

        return "\n".join(observation_list)

    async def _run_tool_async(self, tool_name: str, args_str: str) -> str:
        """
        异步运行单个工具。
        使用 asyncio.to_thread 兼容现有的同步工具。
        """
        try:
            tool = self.registry.get_tool(tool_name)
            # 在单独的线程中运行同步的工具，防止阻塞
            result = await asyncio.to_thread(tool.run, expression=args_str)
            return str(result)
        except (ToolNotFoundError, ToolError) as e:
            return f"Error - {str(e)}"
        except Exception as e:
            return f"Unexpected Error - {str(e)}"
