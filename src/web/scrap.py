from typing import TypedDict, Optional, Any
from playwright.async_api import async_playwright, Playwright
from inscriptis import get_text
from loguru import logger

async def _fetch_website_data(
    playwright: Playwright, url: str
) -> tuple[str | None, str | None, str | None]:
    """
    Se connecte à une URL donnée avec Playwright et retourne le titre et le contenu HTML de la page.

    Args:
        url: L'URL du site web à visiter.

    Returns:
        Un tuple contenant le titre de la page et son contenu HTML.
        Retourne (None, None) si une erreur survient.
    """
    chromium = playwright.chromium
    logger.info("Launching Chromium")
    browser = await chromium.launch()
    page = await browser.new_page()
    try:
        logger.info(f"Visiting {url}")
        await page.goto(url, timeout=60000)  # Timeout de 60 secondes
        title = await page.title()
        content = await page.content()
        text = get_text(content)
        logger.success(f"Retrieved content from {url}")
        return title, content, text
    except Exception as e:
        logger.error(e)
        return None, None, None
    finally:
        # Ferme le navigateur
        await browser.close()

async def read_url(url: str) -> str:
    """Reads the content of a webpage url"""
    async with async_playwright() as playwright:
        title, html_content, text_content = await _fetch_website_data(playwright, url)
    return f"{title}\n===\n{text_content}"
