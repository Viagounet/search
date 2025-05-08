import requests
import base64
import io
import fitz

from urllib.parse import urlparse
from typing import TypedDict


class SearchResult(TypedDict):
    title: str
    url: str
    contains_file: bool


def pdf_stream(url: str) -> io.BytesIO:
    parsed_uri = urlparse(url)
    base_url = f"{parsed_uri.scheme}://{parsed_uri.netloc}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": base_url,
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    pdf_content = response.content
    return io.BytesIO(pdf_content)
