import asyncio
from web.scrap import read_url
from web.search import search

search_results = search("Why is Gawr Gura graduating?")
content = asyncio.run(read_url("https://www.orange.com"))
print(content)
print(search_results)