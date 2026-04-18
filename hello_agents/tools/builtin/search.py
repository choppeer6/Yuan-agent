from duckduckgo_search import DDGS
from ..base import BaseTool
from ...core.exceptions import ToolError

class SearchTool(BaseTool):
    """
    使用 DuckDuckGo 的网络搜索工具。
    """
    def __init__(self):
        super().__init__(
            name="search",
            description="在互联网上搜索信息。例如: search('2024年奥运会金牌榜')"
        )

    def run(self, expression: str, max_results: int = 3) -> str:
        """
        执行搜索并返回前几个结果的摘要。
        """
        # 注意：这里的 expression 实际就是 LLM 传进来的搜索关键词
        query = expression.strip().strip('"').strip("'")
        
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                
            if not results:
                return "No results found for your query."

            # 将结果列表合并为一段可读的文本
            formatted_results = []
            for i, r in enumerate(results):
                formatted_results.append(f"[{i+1}] Title: {r['title']}\nSnippet: {r['body']}\nLink: {r['href']}")
            
            return "\n\n".join(formatted_results)

        except Exception as e:
            # 捕获网络、库内部或 API 相关的各种错误
            raise ToolError(self.name, f"Search failed: {str(e)}")
