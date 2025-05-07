from utils import SearchResult
from scrapping_test import fetch_website_data
from search import search


def get_content(search_results: list[SearchResult]):
    for search_result in search_results:
        title, html_content, text_content = fetch_website_data(search_result["url"])
        print(title)
        print("=============")
        print(text_content)
        input("\n\n\n")


search_results = search("Why is the moon orbiting the earth?", search_lang="en")
get_content(search_results)
