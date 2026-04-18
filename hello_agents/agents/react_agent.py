import re
from typing import Optional, override
from ..core.agent import BaseAgent
from ..core.message import user_message, assistant_message
from ..core.config import settings
from ..core.exceptions import LLMError

class ReActAgent(BaseAgent):
    """
    实现经典的 ReAct (Reason + Act) 模式。
    """

    REACT_SYSTEM_PROMPT = """You are a helpful assistant with access to several tools.
For each user request, follow this format:

Thought: Describe your reasoning about what to do next.
Action: tool_name("arguments")
Observation: The result of the tool execution.
... (Repeat Thought/Action/Observation if needed)
Final Answer: The final response to the user.

Available tools:
{tool_descriptions}
"""

    def __init__(self, llm, tools=None):
        tool_descriptions = tools.list_tools_for_prompt() if tools else "No tools available."
        system_prompt = self.REACT_SYSTEM_PROMPT.format(tool_descriptions=tool_descriptions)
        super().__init__(llm, system_prompt=system_prompt, tools=tools)

    @override
    def run(self, user_input: str, max_steps: int = None) -> str:
        """
        ReAct 的核心循环。
        使用 settings.AGENT_MAX_STEPS 作为默认值。
        """
        steps = max_steps or settings.AGENT_MAX_STEPS
        
        print(f"\n🚀 [ReAct] 开始处理任务: {user_input}")
        self.add_message(user_message(user_input))

        for step in range(steps):
            print(f"\n--- 第 {step + 1} 步 ---")
            
            try:
                # 1. 思考
                response_text = self.llm.think(self.memory)
                self.add_message(assistant_message(response_text))

                # 2. 检查答案
                if "Final Answer:" in response_text:
                    return response_text.split("Final Answer:")[-1].strip()

                # 3. 执行
                observation_text = self.parse_and_execute_action(response_text)
                if observation_text:
                    self.add_message(user_message(observation_text))
                else:
                    msg = "No Action or Final Answer found. Please follow the format."
                    self.add_message(user_message(msg))
            
            except LLMError as e:
                # 处理模型调用异常（如超时或 API 问题）
                print(f"❌ 模型调用出错: {e}")
                return f"Sorry, I encountered an error: {str(e)}"

        return "❌ 达到了最大执行步数，未能得出答案。"
