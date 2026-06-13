import asyncio
from typing import List, Dict  # Missing import that caused the run to fail
from duckduckgo_search import DDGS

class SearchService:
    def __init__(self):
        pass

    def _sync_search(self, query: str, max_results: int) -> List[Dict[str, str]]:
        try:
            with DDGS() as ddgs:
                # Official, updated call that returns the results directly
                results = ddgs.text(keywords=query, max_results=max_results)
                
                if not results:
                    return []
                    
                return [
                    {
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "")
                    }
                    for r in results
                ]
        except Exception as e:
            print(f"Internal Sync Search Error: {str(e)}")
            return []

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        return await asyncio.to_thread(
            self._sync_search, 
            query, 
            max_results
        )