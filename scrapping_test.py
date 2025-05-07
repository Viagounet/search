from playwright.sync_api import sync_playwright
from inscriptis import get_text


def fetch_website_data(url: str) -> tuple[str | None, str | None, str | None]:
    """
    Se connecte à une URL donnée avec Playwright et retourne le titre et le contenu HTML de la page.

    Args:
        url: L'URL du site web à visiter.

    Returns:
        Un tuple contenant le titre de la page et son contenu HTML.
        Retourne (None, None) si une erreur survient.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            print(f"Connexion à {url}...")
            # Effectue la requête GET sur l'URL
            # Augmentation du timeout par défaut si nécessaire pour les pages lentes
            page.goto(url, timeout=60000)  # Timeout de 60 secondes

            # Récupère le titre de la page
            title = page.title()
            print(f"Le titre de la page est : '{title}'")

            # Récupère le contenu HTML complet de la page
            content = page.content()
            # print(f"Contenu de la page :\n{content[:500]}...") # Affiche les 500 premiers caractères

            text = get_text(content)
            return title, content, text
        except Exception as e:
            print(f"Une erreur est survenue lors de la connexion à {url}: {e}")
            return None, None, None
        finally:
            # Ferme le navigateur
            browser.close()
