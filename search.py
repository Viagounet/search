import os
import requests
import sys

from loguru import logger
from typing import TypedDict, Optional

logger.remove()
logger.level("SEARCH", no=15, color="<blue>", icon="🧐")
logger.add(
    sys.stderr,
    format="<green>{time:HH:mm:ss}</green> | <level>{level.icon} {level.name: <8}</level> | <level>{message}</level>",
)


class SearchResult(TypedDict):
    title: str
    url: str
    contains_file: bool


def search(
    question: str,
    country: str = "US",
    search_lang: str = "en",
    time_range: Optional[tuple[str, str]] = None,
    pdf: bool = False,
    website: Optional[str] = None,
) -> list[SearchResult]:
    question_uri_format = question.replace(" ", "+").lower()
    time_range_parameter = ""
    if time_range:
        if type(time_range) != tuple:
            raise Exception("time_range format should be a tuple of strings")
        time_range_parameter = f"?freshness={time_range[0]}to{time_range[1]}"

    operators = []
    if pdf:
        operators.append("filetype:pdf")
    if website:
        operators.append(f"site:{website}")
    full_search = question + " AND ".join(operators)
    url = f"https://api.search.brave.com/res/v1/web/search?q={full_search}?country={country}?search_lang={search_lang}"

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",  # requests handles gzip decompression automatically
        "X-Subscription-Token": os.environ["BRAVE_API_KEY"],
    }

    logger.log("SEARCH", f"Searching for {full_search}")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    json_response = response.json()
    search_results: list[SearchResult] = []
    if "web" not in json_response:
        return []
    for result in json_response["web"]["results"]:
        search_result: SearchResult = {
            "title": result["title"],
            "url": result["url"],
            "contains_file": True if ".pdf" in result["url"] else False,
        }
        search_results.append(search_result)
    return search_results
