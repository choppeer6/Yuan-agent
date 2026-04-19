import ast
import operator
from ..base import BaseTool
from ...core.exceptions import ToolError

class CalculatorTool(BaseTool):
    """
    一个安全的计算器工具，使用 AST 解析数学表达式。
    """

    # 支持的运算符映射
    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def __init__(self):
        super().__init__(
            name="calculator",
            description="计算数学表达式。例如: calculator(1 + 1)"
        )

    def _safe_eval(self, node):
        """递归地安全求值 AST 节点"""
        if isinstance(node, ast.Expression):
            return self._safe_eval(node.body)
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._OPERATORS:
                raise ToolError(self.name, f"不支持的运算符: {op_type.__name__}")
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            return self._OPERATORS[op_type](left, right)
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._OPERATORS:
                raise ToolError(self.name, f"不支持的运算符: {op_type.__name__}")
            operand = self._safe_eval(node.operand)
            return self._OPERATORS[op_type](operand)
        else:
            raise ToolError(self.name, f"不支持的表达式类型: {type(node).__name__}")

    def run(self, expression: str) -> str:
        try:
            tree = ast.parse(expression.strip(), mode='eval')
            result = self._safe_eval(tree)
            return str(result)
        except ToolError:
            raise
        except Exception as e:
            raise ToolError(self.name, str(e))
