from typing import List, Any
from ..core.agent import BaseAgent

class AgentChain:
    """
    智能体链：顺序执行多个智能体，将前一个 Agent 的输出作为后一个 Agent 的输入。
    """
    def __init__(self, agents: List[BaseAgent]):
        self.agents = agents

    async def run(self, initial_input: str) -> str:
        """
        异步顺序运行整个链条
        """
        current_input = initial_input
        
        print(f"⛓️ 开始执行链式任务，共 {len(self.agents)} 个环节")
        
        for i, agent in enumerate(self.agents):
            agent_name = agent.__class__.__name__
            print(f"  [环节 {i+1}/{len(self.agents)}] 正在调用: {agent_name}...")
            
            # 执行当前智能体
            current_input = await agent.run(current_input)
            
            # 如果中间环节有特殊输出需求，可以在这里扩展
            
        print("✅ 链式任务执行完毕")
        return current_input

# 别名，方便使用
Chain = AgentChain
