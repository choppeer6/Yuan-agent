from typing import TypedDict, List, Optional

class Message(TypedDict):
    """
    基础消息格式，兼容 OpenAI 规范。
    """
    role: str      # 'system', 'user', 'assistant', 'tool'
    content: str
    name: Optional[str] = None # 用于标识 tool 调用者的名字

def system_message(content: str) -> Message:
    return {"role": "system", "content": content}

def user_message(content: str) -> Message:
    return {"role": "user", "content": content}

def assistant_message(content: str) -> Message:
    return {"role": "assistant", "content": content}

def tool_message(content: str, name: str) -> Message:
    return {"role": "tool", "content": content, "name": name}
