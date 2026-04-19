from typing import List, override
from ..core.agent import BaseAgent
from ..core.message import user_message, assistant_message

class ReflectionAgent(BaseAgent):
    """
    实现 Reflection (反思) 模式。
    通过 生成 -> 反思 -> 修正 的循环来提高输出质量。
    """

    GENERATE_PROMPT = "Please provide a detailed answer to the following task:\n{task}"
    REFLECT_PROMPT = "Critique your previous response. Be harsh. Find any errors, inefficiencies, or areas for improvement."
    REFINE_PROMPT = "Based on your critique, provide an improved and final version of your answer."

    def __init__(self, llm, tools=None):
        # Reflection Agent 通常更倾向于创作或复杂逻辑，可以自定义初始系统提示
        super().__init__(llm, system_prompt="You are an expert who strives for perfection through self-reflection.", tools=tools)

    @override
    async def run(self, user_input: str, iterations: int = 1) -> str:
        """
        异步运行反思循环。
        """
        # 1. 初始化生成
        print(f"\n🚀 [Reflection] 初始生成任务: {user_input}")
        self.add_message(user_message(self.GENERATE_PROMPT.format(task=user_input)))
        
        # 调用 LLM 生成第一个版本
        response = await self.llm.astream_chat(self.memory)
        self.add_message(assistant_message(response))
        
        # 2. 循环反思
        for i in range(iterations):
            print(f"🔄 [Reflection] 正在进行第 {i+1} 轮反思...")
            
            # 添加反思指令
            self.add_message(user_message(self.REFLECT_PROMPT))
            
            # LLM 反思
            critique = await self.llm.astream_chat(self.memory)
            self.add_message(assistant_message(critique))
            
            print(f"📝 [Reflection] 反思意见已生成，正在修正...")
            
            # 添加修正指令
            self.add_message(user_message(self.REFINE_PROMPT))
            
            # LLM 修正
            response = await self.llm.astream_chat(self.memory)
            self.add_message(assistant_message(response))
            
        print("✅ [Reflection] 任务已通过反思优化")
        return response
