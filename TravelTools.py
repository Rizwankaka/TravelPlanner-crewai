from duckduckgo_search import DDGS
from typing import List, Dict, Any
from crewai.tools import BaseTool

class DuckDuckGoSearchTool(BaseTool):
    """Tool for searching DuckDuckGo."""
    
    name: str = "duckduckgo_search"
    description: str = "Search the web for information using DuckDuckGo"
    
    def __init__(self):
        super().__init__()
    
    def _run(self, query: str) -> str:
        """
        Search the web using DuckDuckGo.
        
        Args:
            query: The search query.
            
        Returns:
            Formatted string of search results.
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                return self.process_search_results(results)
        except Exception as e:
            return f"Error performing search: {str(e)}"
    
    def process_search_results(self, results: List[Dict[str, Any]]) -> str:
        """
        Process search results into a readable format.
        
        Args:
            results: List of search results.
            
        Returns:
            Formatted string of search results.
        """
        if not results:
            return "No results found."
        
        if isinstance(results, list) and len(results) > 0 and isinstance(results[0], dict) and "error" in results[0]:
            return results[0]["error"]
        
        formatted_results = ""
        for i, result in enumerate(results, 1):
            formatted_results += f"{i}. {result.get('title', 'No title')}\n"
            formatted_results += f"   Link: {result.get('href', 'No link')}\n"
            formatted_results += f"   {result.get('body', 'No snippet')}\n\n"
        
        return formatted_results

class SearchTools:
    """Tools for searching information on the web."""
    
    def __init__(self):
        self.duckduckgo_search = DuckDuckGoSearchTool()