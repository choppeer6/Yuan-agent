from typing import override
from ..core.agent import BaseAgent
from ..core.message import user_message, assistant_message

class SimpleAgent(BaseAgent):
    """
    最基础的 Agent：只负责直接对话，不进行复杂的工具调用或推理循环。
    适用于简单的问答、聊天或作为链条中的一个环节。
    """
    
    @override
    async def run(self, user_input: str) -> str:
        """
        简单的异步对话逻辑
        """
        # 1. 记录用户输入
        self.add_message(user_message(user_input))
        
        # 2. 调用 LLM 获取回复
        response = await self.llm.astream_chat(self.memory)
        
        # 3. 记录并返回助手回复
        self.add_message(assistant_message(response))
        
        return response
