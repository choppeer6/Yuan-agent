class HelloAgentsError(Exception):
    """框架所有异常的基类"""
    pass

class LLMError(HelloAgentsError):
    """LLM 调用相关的异常"""
    def __init__(self, message: str, details: str = None):
        super().__init__(message)
        self.details = details

class ToolError(HelloAgentsError):
    """工具执行相关的异常"""
    def __init__(self, tool_name: str, message: str):
        super().__init__(f"Tool '{tool_name}' failed: {message}")
        self.tool_name = tool_name

class AgentStepError(HelloAgentsError):
    """Agent 步进逻辑相关的异常"""
    pass

class ToolNotFoundError(ToolError):
    """找不到指定的工具"""
    def __init__(self, tool_name: str):
        super().__init__(tool_name, "Tool not found in registry.")
