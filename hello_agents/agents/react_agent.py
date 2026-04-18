import re
from typing import Optional, override
from ..core.agent import BaseAgent
from ..core.message import user_message, assistant_message

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
        # 自动生成包含工具描述的 System Prompt
        tool_descriptions = tools.list_tools_for_prompt() if tools else "No tools available."
        system_prompt = self.REACT_SYSTEM_PROMPT.format(tool_descriptions=tool_descriptions)
        super().__init__(llm, system_prompt=system_prompt, tools=tools)

    @override
    def run(self, user_input: str, max_steps: int = 5) -> str:
        """
        ReAct 的核心循环。
        """
        print(f"\n🚀 开始处理任务: {user_input}")
        self.add_message(user_message(user_input))

        for step in range(max_steps):
            print(f"\n--- 第 {step + 1} 步 ---")
            
            # 1. 思考并决定下一步行为
            response_text = self.llm.think(self.memory)
            if not response_text:
                return "❌ 调用 LLM 失败。"
            
            self.add_message(assistant_message(response_text))

            # 2. 检查是否已有最终答案
            if "Final Answer:" in response_text:
                return response_text.split("Final Answer:")[-1].strip()

            # 3. 尝试解析并执行 Action
            observation_text = self.parse_and_execute_action(response_text)
            if observation_text:
                print(f"👁️ 观察到结果: {observation_text}")
                self.add_message(user_message(observation_text))
            else:
                # 如果没找到 Action 也没有 Final Answer，提醒模型
                msg = "No Action or Final Answer found. Please follow the format."
                self.add_message(user_message(msg))

        return "❌ 达到了最大执行步数，未能得出答案。"
