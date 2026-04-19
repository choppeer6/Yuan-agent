from typing import Dict, List, Optional, override
from ..core.agent import BaseAgent
from ..core.message import user_message, assistant_message

class ManagerAgent(BaseAgent):
    """
    管理者智能体：负责理解任务并从自己的“代理池”中选择最合适的 Agent 去解决。
    这实现了任务的分流和专业化分工。
    """
    def __init__(self, llm, agents_pool: Dict[str, BaseAgent], system_prompt: str = None):
        # 默认系统提示词，告诉 Manager 它有哪些资源
        agents_info = "\n".join([f"- {name}: {agent.__class__.__name__}" for name, agent in agents_pool.items()])
        default_prompt = f"""You are a Task Manager. Your job is to analyze user tasks and dispatch them to the most suitable agent.
Available Agents:
{agents_info}

Instructions:
1. Identify the core intent of the user request.
2. Select the name of the best agent to handle the request.
3. Your response MUST be in this format: [AGENT_NAME] : [REFINED_TASK_FOR_AGENT]
"""
        super().__init__(llm, system_prompt or default_prompt)
        self.agents_pool = agents_pool

    @override
    async def run(self, user_input: str) -> str:
        """
        Manager 的运行逻辑：分析 -> 派发 -> 返回结果
        """
        # 1. 记录并询问 LLM 该找谁
        self.add_message(user_message(f"Current Task: {user_input}"))
        
        # 2. 获取 LLM 的指派决策
        decision = await self.llm.astream_chat(self.memory)
        self.add_message(assistant_message(decision))
        
        # 3. 解析决策 (格式: [AGENT_NAME] : [TASK])
        try:
            if ":" in decision:
                parts = decision.split(":", 1)
                agent_name = parts[0].strip().replace("[", "").replace("]", "")
                refined_task = parts[1].strip()
            else:
                # 容错：如果 LLM 没按格式给，尝试匹配已有的 agent 名称
                agent_name = next((name for name in self.agents_pool.keys() if name.lower() in decision.lower()), None)
                refined_task = user_input
                
            if agent_name in self.agents_pool:
                target_agent = self.agents_pool[agent_name]
                print(f"👨‍💼 Manager 决定指派任务给: {agent_name}")
                # 4. 调用目标 Agent 执行任务
                result = await target_agent.run(refined_task)
                return result
            else:
                return f"Manager Error: No suitable agent found for '{agent_name}'. Full decision: {decision}"
                
        except Exception as e:
            return f"Manager failed to dispatch task: {str(e)}"
