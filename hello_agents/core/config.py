import os
from pathlib import Path
from dotenv import load_dotenv

# 自动定位项目根目录并加载 .env
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    """
    Agent 框架全局配置类
    """
    
    # --- LLM 配置 ---
    LLM_MODEL_ID: str = os.getenv("LLM_MODEL_ID", "gpt-3.5-turbo")
    LLM_API_KEY: str = os.getenv("LLM_API_KEY", "")
    LLM_BASE_URL: str = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", 60))
    LLM_MAX_RETRIES: int = int(os.getenv("LLM_MAX_RETRIES", 3))

    # --- Agent 运行配置 ---
    AGENT_MAX_STEPS: int = int(os.getenv("AGENT_MAX_STEPS", 10))
    AGENT_DEFAULT_TEMPERATURE: float = float(os.getenv("AGENT_DEFAULT_TEMPERATURE", 0.7))
    
    # --- 日志与调试 ---
    DEBUG: bool = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")

    def validate(self):
        """校验关键配置是否存在"""
        if not self.LLM_API_KEY:
            print("⚠️ 警告: LLM_API_KEY 未配置，Agent 可能无法正常运行。")
        if not self.LLM_MODEL_ID:
            print("⚠️ 警告: LLM_MODEL_ID 未配置。")

# 实例化单例
settings = Settings()
settings.validate()
