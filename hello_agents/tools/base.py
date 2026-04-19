from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseTool(ABC):
    """
    所有工具的基类。
    """
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    @abstractmethod
    def run(self, **kwargs) -> Any:
        """
        工具的执行逻辑。
        """
        pass

    def to_prompt(self) -> str:
        """
        将工具信息转换成 Prompt 中的描述。
        """
        return f"{self.name}: {self.description}"
