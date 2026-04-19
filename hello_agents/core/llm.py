from openai import AsyncOpenAI
from typing import List, Dict, Optional, Any
from .config import settings
from .exceptions import LLMError
from .message import Message

class HelloAgentsLLM:
    """
    为本书 "Hello Agents" 定制的LLM客户端。
    支持同步和异步调用，兼容 OpenAI 接口。
    """

    def __init__(self, model: str = None, api_key: str = None, base_url: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从 settings 加载。
        """
        self.model = model or settings.LLM_MODEL_ID
        api_key = api_key or settings.LLM_API_KEY
        base_url = base_url or settings.LLM_BASE_URL
        timeout = timeout or settings.LLM_TIMEOUT

        if not all([self.model, api_key, base_url]):
            raise LLMError("模型ID、API密钥和服务地址必须被提供或在配置中定义。")

        # 同时初始化同步和异步客户端
        self.client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    async def astream_chat(self, messages: List[Message], temperature: float = None) -> str:
        """
        异步流式调用大语言模型。
        """
        temp = temperature if temperature is not None else settings.AGENT_DEFAULT_TEMPERATURE
        
        # 将 Message 对象转换为 OpenAI 要求的字典格式
        formatted_messages = [{"role": m.role, "content": m.content} for m in messages]

        if settings.DEBUG:
            print(f"🧠 [Async Debug] 正在调用 {self.model} 模型 (Temp: {temp})...")

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temp,
                stream=True,
            )

            collected_content = []
            async for chunk in response:
                content = chunk.choices[0].delta.content or ""
                if settings.DEBUG:
                    print(content, end="", flush=True)
                collected_content.append(content)

            if settings.DEBUG:
                print()  # 换行

            return "".join(collected_content)

        except Exception as e:
            raise LLMError(f"异步调用LLM API时发生错误: {e}")

    async def athink(self, messages: List[Dict[str, str]], temperature: float = None) -> str:
        """
        athink 是 astream_chat 的别名或简化版，接收字典格式的输入。
        """
        temp = temperature if temperature is not None else settings.AGENT_DEFAULT_TEMPERATURE
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temp,
                stream=False,
            )
            return response.choices[0].message.content
        except Exception as e:
            raise LLMError(f"异步调用LLM (athink) 时发生错误: {e}")

    def think(self, messages: List[Dict[str, str]], temperature: float = None) -> str:
        """
        保留同步调用方法（虽然内部现在建议使用异步）。
        为了简单起见，这里可以抛出一个提示或保持原有逻辑（但需要同步客户端）。
        由于我们主要走异步流程，这里建议尽量使用 athink 或 astream_chat。
        """
        import asyncio
        # 这是一个 hack 手段，在同步环境中调用异步方法
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        return loop.run_until_complete(self.athink(messages, temperature))
