from typing import Any

import trafilatura
from ddgs import DDGS
from langchain_core.tools import tool

from config import MAX_WEB_SEARCH_RESULTS, MAX_WEB_SEARCH_PAGE_SYMBOLS
from agents.web_subagent.schemas import WebSearchSchema




@tool(args_schema=WebSearchSchema)
def web_search(**kwargs: dict[str, Any]) -> str:
    """
    Tool to search the web for information.
    """

    query = kwargs["query"]

    results = DDGS().text(query, max_results=MAX_WEB_SEARCH_RESULTS)

    urls = [result["href"] for result in results]

    pages = []

    for url in urls:

        downloaded = trafilatura.fetch_url(url)

        if downloaded is None:

            pages.append(f"Could not download the page from {url}.")

            continue

        text = trafilatura.extract(downloaded)

        if text is None:

            pages.append(f"Could not extract the text from the page from {url}.")

            continue

        pages.append(text[:MAX_WEB_SEARCH_PAGE_SYMBOLS])

    return "\n\n".join(pages)



web_subagent_tools = [web_search]