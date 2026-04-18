from ..base import BaseTool

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
            # 这是一个简单的 eval，实际应用中建议使用更安全的数学表达式解析器
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Error: {e}"
