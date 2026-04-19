import re
import asyncio
from typing import List, Optional, override
from .llm import HelloAgentsLLM
from .message import Message, system_message, user_message
from .config import settings
from .exceptions import ToolError, ToolNotFoundError, LLMError
from ..tools.registry import ToolRegistry
from ..tools.async_executor import AsyncExecutor

class BaseAgent:
    """
    所有 Agent 的基类。
    升级为支持异步 (Async) 并发执行。
    """
    def __init__(
        self, 
        llm: HelloAgentsLLM, 
        system_prompt: str = "You are a helpful assistant.",
        tools: Optional[ToolRegistry] = None
    ):
        self.llm = llm
        self.system_prompt = system_prompt
        self.tools = tools or ToolRegistry()
        # 核心：引入异步执行器
        self.executor = AsyncExecutor(self.tools)
        self.memory: List[Message] = [system_message(self.system_prompt)]

    def add_message(self, message: Message):
        self.memory.append(message)

    def reset_memory(self):
        self.memory = [system_message(self.system_prompt)]

    async def run(self, user_input: str) -> str:
        """
        Agent 的异步运行逻辑，具体逻辑由子类实现。
        """
        raise NotImplementedError("子类必须实现异步 run 方法")
