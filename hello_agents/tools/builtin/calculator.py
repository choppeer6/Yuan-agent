from ..base import BaseTool
from ...core.exceptions import ToolError

class CalculatorTool(BaseTool):
    """
    一个简单的计算器工具。
    """
    def __init__(self):
        super().__init__(
            name="calculator",
            description="计算数学表达式。例如: calculator(1 + 1)"
        )

    def run(self, expression: str) -> str:
        try:
            # 实际应用中建议使用更安全的数学表达式解析器
            result = eval(expression)
            return str(result)
        except Exception as e:
            # 统一抛出 ToolError
            raise ToolError(self.name, str(e))
