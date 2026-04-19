from typing import Optional, override
from ..core.agent import BaseAgent
from ..core.message import user_message, assistant_message
from ..core.config import settings

class PlanSolveAgent(BaseAgent):
    """
    实现 Plan-and-Solve 模式。
    """

    PLAN_SYSTEM_PROMPT = """You are a helpful assistant with access to several tools.
For any given task, you must first create a detailed step-by-step plan.
Then, execute each step one by one using tools.

Available tools:
{tool_descriptions}

Format for Planning:
Plan: 
1. step one...
2. step two...

Format for Execution:
Thought: Based on the plan and observations, what should I do now?
Action: tool_name("arguments")
Observation: Result...
...
Final Answer: The final response to the user.
"""

    def __init__(self, llm, tools=None):
        tool_descriptions = tools.list_tools_for_prompt() if tools else "No tools available."
        system_prompt = self.PLAN_SYSTEM_PROMPT.format(tool_descriptions=tool_descriptions)
        super().__init__(llm, system_prompt=system_prompt, tools=tools)

    @override
    async def run(self, user_input: str, max_steps: int = None) -> str:
        """
        异步版 Plan-and-Solve 的运行逻辑。
        """
        steps = max_steps or settings.AGENT_MAX_STEPS

        print(f"\n🚀 [Plan-and-Solve] 开始处理任务: {user_input}")
        self.add_message(user_message(user_input))

        # 1. 制定计划
        print("\n📝 正在制定计划...")
        plan_response = await self.llm.athink(self.memory)
        if not plan_response:
            return "❌ 制定计划失败。"
        
        self.add_message(assistant_message(plan_response))

        # 2. 依次执行步骤
        for step in range(steps):
            print(f"\n--- 执行步骤 {step + 1} ---")
            
            # 引导模型根据计划继续
            prompt = "Please proceed with the next step of the plan."
            self.add_message(user_message(prompt))
            
            response_text = await self.llm.athink(self.memory)
            if not response_text:
                return "❌ 执行过程中调用 LLM 失败。"
            
            self.add_message(assistant_message(response_text))

            # 检查是否已有最终答案
            if "Final Answer:" in response_text:
                return response_text.split("Final Answer:")[-1].strip()

            # 使用 AsyncExecutor 执行工具（替代原来不存在的 parse_and_execute_action）
            observation_text = await self.executor.execute_all(response_text)
            if observation_text:
                if settings.DEBUG:
                    print(f"👁️ 观察到结果: {observation_text}")
                self.add_message(user_message(observation_text))
            else:
                # 如果没有 Action 也没有 Final Answer，提醒它按照计划执行
                print("⚠️ 未发现 Action 或 Final Answer，请求模型明确下一步。")

        return "❌ 达到了最大执行步数，未能得出答案。"
