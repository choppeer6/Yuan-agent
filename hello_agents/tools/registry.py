from typing import Dict, List
from .base import BaseTool

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
        return self._tools.get(name)

    def list_tools_for_prompt(self) -> str:
        """
        生成给 LLM 看的工具说明列表。
        """
        return "\n".join([tool.to_prompt() for tool in self._tools.values()])

    def get_all_tools(self) -> List[BaseTool]:
        return list(self._tools.values())
