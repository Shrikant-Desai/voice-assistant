import requests
from config import NEWS_API_KEY, NEWS_COUNTRY, NEWS_MAX_ARTICLES
from utils.logger import get_logger

logger = get_logger(__name__)

NEWS_URL = (
    f"https://newsapi.org/v2/top-headlines"
    f"?country={NEWS_COUNTRY}&apiKey={NEWS_API_KEY}"
)


def fetch_headlines() -> list[str]:
    """Fetch top news headlines. Returns list of title strings."""
    try:
        response = requests.get(NEWS_URL, timeout=5)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        headlines = [a["title"] for a in articles if a.get("title")]
        logger.info(f"Fetched {len(headlines)} headlines.")
        return headlines[:NEWS_MAX_ARTICLES]

    except requests.RequestException as e:
        logger.error(f"News API error: {e}")
        return []
