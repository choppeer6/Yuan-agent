import re
from typing import List, Optional, override
from .llm import HelloAgentsLLM
from .message import Message, system_message, user_message
from ..tools.registry import ToolRegistry

class BaseAgent:
    """
    所有 Agent 的基类。
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
        self.memory: List[Message] = [system_message(self.system_prompt)]

    def add_message(self, message: Message):
        """将消息添加到记忆中"""
        self.memory.append(message)

    def reset_memory(self):
        """重置记忆，只保留系统提示词"""
        self.memory = [system_message(self.system_prompt)]

    def parse_and_execute_action(self, text: str) -> Optional[str]:
        """
        通用的工具调用解析逻辑。
        匹配格式: Action: tool_name("arguments")
        """
        action_match = re.search(r'Action:\s*(\w+)\((.*)\)', text)
        if action_match:
            tool_name = action_match.group(1)
            tool_args_str = action_match.group(2).strip().strip('"').strip("'")
            
            print(f"🛠️ 准备调用工具: {tool_name}({tool_args_str})")
            
            tool = self.tools.get_tool(tool_name)
            if tool:
                try:
                    observation = tool.run(expression=tool_args_str)
                    return f"Observation: {observation}"
                except Exception as e:
                    return f"Observation: Error executing tool: {e}"
            else:
                return f"Observation: Tool '{tool_name}' not found."
        return None

    def run(self, user_input: str) -> str:
        """
        Agent 的主运行逻辑，具体逻辑由子类实现。
        """
        raise NotImplementedError("子类必须实现 run 方法")
