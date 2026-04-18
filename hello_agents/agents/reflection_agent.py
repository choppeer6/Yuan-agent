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
    def run(self, user_input: str, iterations: int = 1) -> str:
        """
        Reflection 的运行逻辑。
        iterations: 反思的轮数。
        """
        print(f"\n🚀 [Reflection] 开始处理任务: {user_input}")
        
        # 1. 初始生成
        print("\n🎨 正在生成初始草案...")
        self.add_message(user_message(self.GENERATE_PROMPT.format(task=user_input)))
        draft = self.llm.think(self.memory)
        self.add_message(assistant_message(draft))

        current_content = draft

        for i in range(iterations):
            print(f"\n--- 反思轮次 {i + 1} ---")

            # 2. 自我反思
            print("🔍 正在进行自我批评...")
            self.add_message(user_message(self.REFLECT_PROMPT))
            critique = self.llm.think(self.memory)
            self.add_message(assistant_message(critique))

            # 3. 根据反思进行修正
            print("🛠️ 正在根据反馈进行优化...")
            self.add_message(user_message(self.REFINE_PROMPT))
            refined_content = self.llm.think(self.memory)
            self.add_message(assistant_message(refined_content))
            
            current_content = refined_content

        print("\n✅ 反思循环完成。")
        return current_content
