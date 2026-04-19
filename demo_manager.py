import asyncio
from hello_agents.core.llm import HelloAgentsLLM
from hello_agents.tools.registry import ToolRegistry
from hello_agents.tools.builtin.calculator import CalculatorTool
from hello_agents.tools.builtin.search import SearchTool
from hello_agents.agents.react_agent import ReActAgent
from hello_agents.agents.reflection_agent import ReflectionAgent
from hello_agents.agents.manager_agent import ManagerAgent
from hello_agents.core.config import settings

async def main():
    # 0. 环境设置
    settings.DEBUG = True
    llm = HelloAgentsLLM()
    
    # 1. 准备工具和专家池
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(SearchTool())
    
    # 创建专家
    searcher = ReActAgent(llm=llm, tools=registry)
    writer = ReflectionAgent(llm=llm)
    
    # 2. 初始化管理者
    agents_pool = {
        "Searcher": searcher,
        "Writer": writer
    }
    
    manager = ManagerAgent(llm=llm, agents_pool=agents_pool)
    
    print("\n" + "="*50)
    print("🤖 Yuan-agent 多智能体协作演示")
    print("="*50)

    # --- 场景 1: 复杂查询与计算 (应指派给 Searcher) ---
    print("\n>>> [场景 1] 复杂查询与计算")
    task_1 = "帮我查一下目前黄金的价格，并计算如果我有 1.5 盎司黄金，总价值是多少美元？"
    result_1 = await manager.run(task_1)
    print(f"\n✅ 最终回复: {result_1}")

    print("\n" + "-"*30)

    # --- 场景 2: 高质量写作与反思 (应指派给 Writer) ---
    print("\n>>> [场景 2] 高质量写作与反思")
    task_2 = "请帮我写一篇关于‘人工智能如何改变未来工作模式’的短评，要有深度且引人思考。"
    result_2 = await manager.run(task_2)
    print(f"\n✅ 最终回复: {result_2}")

if __name__ == "__main__":
    asyncio.run(main())
