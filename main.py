from hello_agents.core.llm import HelloAgentsLLM
from hello_agents.tools.registry import ToolRegistry
from hello_agents.tools.builtin.calculator import CalculatorTool
from hello_agents.agents.react_agent import ReActAgent
from hello_agents.agents.plan_solve_agent import PlanSolveAgent
from hello_agents.agents.reflection_agent import ReflectionAgent

def main():
    # 1. 初始化 LLM
    llm = HelloAgentsLLM()

    # 2. 准备工具
    registry = ToolRegistry()
    registry.register(CalculatorTool())

    # --- 演示 ReAct ---
    # task_math = "我有 5000 元，买了 3 台单价为 1299 元的打印机，剩下的钱刚好够买几盒单价为 45 元的墨盒？"
    # react_agent = ReActAgent(llm=llm, tools=registry)
    # react_agent.run(task_math)

    # --- 演示 Reflection ---
    print("\n" + "="*20 + " 演示 Reflection Agent " + "="*20)
    task_code = "用 Python 实现一个函数计算斐波那契数列第 n 项的值。"
    reflection_agent = ReflectionAgent(llm=llm)
    # 运行 1 轮反思（生成 -> 反思 -> 修正）
    reflection_result = reflection_agent.run(task_code, iterations=1)
    
    print(f"\n✅ Reflection 最终输出:\n{reflection_result}")

if __name__ == "__main__":
    main()
