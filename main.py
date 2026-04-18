from hello_agents.core.llm import HelloAgentsLLM
from hello_agents.tools.registry import ToolRegistry
from hello_agents.tools.builtin.calculator import CalculatorTool
from hello_agents.tools.builtin.search import SearchTool
from hello_agents.agents.react_agent import ReActAgent
from hello_agents.agents.plan_solve_agent import PlanSolveAgent

def main():
    # 1. 初始化 LLM
    llm = HelloAgentsLLM()

    # 2. 准备工具
    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(SearchTool())

    # 3. 准备任务：需要联网获取实时信息并计算
    task = "当前 1 美元兑换人民币的汇率是多少？如果我有 500 美元，我能换到多少人民币？"

    print("="*20 + " 演示 ReAct Agent (带搜索) " + "="*20)
    # 我们可以通过设置 settings.DEBUG = True 来查看详细的工具调用过程
    from hello_agents.core.config import settings
    settings.DEBUG = True 
    
    agent = ReActAgent(llm=llm, tools=registry)
    result = agent.run(task)
    
    print(f"\n✅ 最终答案: {result}")

if __name__ == "__main__":
    main()
