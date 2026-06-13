import asyncio
import time
import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

class SearchService:
    def __init__(self):
        pass

    def _normalize_query(self, query: str) -> str:
        original = query.strip()
        if not original:
            return original

        lower_query = original.lower()
        if "שמות הפילים" in lower_query and "רמת גן" in lower_query:
            return "שמות הפילים בספארי רמת גן רשימה מלאה"

        list_indicators = ["list", "names", "data", "רשימה", "שמות", "נתונים", "מידע"]
        question_indicators = ["?", "who", "what", "where", "when", "how", "why", "מי", "מה", "איפה", "מתי", "למה", "איך", "כיצד"]

        if any(term in lower_query for term in list_indicators):
            return original

        if any(term in lower_query for term in question_indicators):
            return f"{original} list names data"

        return original

    def _scrape_full_content(self, url: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            time.sleep(3)
            
            soup = BeautifulSoup(response.text, "html.parser")
            text_content = soup.get_text(separator=" ", strip=True)
            
            return text_content[:2000] if text_content else ""
        except Exception as e:
            print(f"Scrape content error for {url}: {str(e)}")
            return ""

    def _sync_search(self, query: str, max_results: int) -> List[Dict[str, str]]:
        query = self._normalize_query(query)
        try:
            with DDGS() as ddgs:
                results = ddgs.text(keywords=query, max_results=max_results)
                
                formatted_results = []
                for r in results:
                    formatted_results.append({
                        "title": r.get("title", ""),
                        "url": r.get("href", ""),
                        "snippet": r.get("body", "")
                    })
                
                # שיפור: נחפש לינק איכותי במקום לקחת את הראשון באקראי
                trusted_sources = ["wikipedia", "gov.il", "ynet", "walla", "haaretz"]
                for res in formatted_results:
                    url = res.get("url", "").lower()
                    if any(source in url for source in trusted_sources):
                        print(f"DEBUG: Found trusted source: {url}")
                        full_content = self._scrape_full_content(url)
                        if full_content:
                            res["snippet"] = full_content
                        break # מצאנו מקור אמין, אפשר לעצור
                
                return formatted_results
        except Exception as e:
            print(f"Internal Sync Search Error: {str(e)}")
            return []

    async def search_web(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        return await asyncio.to_thread(
            self._sync_search, 
            query, 
            max_results
        )