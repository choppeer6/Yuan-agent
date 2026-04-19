from typing import Dict, List
from .base import BaseTool
from ..core.exceptions import ToolNotFoundError

class ToolRegistry:
    """
    管理所有可用工具的注册表。
    """
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}

    def register(self, tool: BaseTool):
        self._tools[tool.name] = tool
        print(f"🛠️ 工具已注册: {tool.name}")

    def get_tool(self, name: str) -> BaseTool:
        if name not in self._tools:
            raise ToolNotFoundError(name)
        return self._tools[name]

    def list_tools_for_prompt(self) -> str:
        return "\n".join([tool.to_prompt() for tool in self._tools.values()])

    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())
