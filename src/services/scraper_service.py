import asyncio
import requests
from bs4 import BeautifulSoup

class ScraperService:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5"
        }

    def _sync_scrape(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, allow_redirects=True, timeout=10.0)
            if response.status_code != 200:
                return f"Error: Unable to fetch URL (Status Code: {response.status_code})"
            
            soup = BeautifulSoup(response.text, "html.parser")
            for script_or_style in soup(["script", "style", "nav", "footer", "header", "aside"]):
                script_or_style.decompose()
            
            raw_text = soup.get_text()
            lines = (line.strip() for line in raw_text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = "\n".join(chunk for chunk in chunks if chunk)
            
            return clean_text[:4000]
            
        except requests.Timeout:
            return "Error: The request timed out while trying to reach the URL."
        except Exception as e:
            return f"Error while parsing URL: {str(e)}"

    async def scrape_url(self, url: str) -> str:
        return await asyncio.to_thread(self._sync_scrape, url)