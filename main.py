import asyncio
from hello_agents.core.llm import HelloAgentsLLM
from hello_agents.tools.registry import ToolRegistry
from hello_agents.tools.builtin.calculator import CalculatorTool
from hello_agents.tools.builtin.search import SearchTool
from hello_agents.agents.react_agent import ReActAgent
from hello_agents.core.config import settings

async def main():
    # 1. 初始化 LLM
    llm = HelloAgentsLLM()

    # 2. 准备工具
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(SearchTool())

    # 3. 准备并发搜索任务
    task = "同时查找并对比：华为 Mate 60 Pro、小米 14 Ultra 和 iPhone 15 Pro 的处理器型号是什么？"

    print("="*20 + " 演示并发 Async ReAct Agent " + "="*20)
    settings.DEBUG = True 
    
    agent = ReActAgent(llm=llm, tools=registry)
    
    # 异步运行
    result = await agent.run(task)
    
    print(f"\n✅ 最终答案: {result}")

if __name__ == "__main__":
    # 使用 asyncio.run 运行异步主函数
    asyncio.run(main())
