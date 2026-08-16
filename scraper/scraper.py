import requests
from bs4 import BeautifulSoup
import mysql.connector

from ai_classifier import predict_category


def scrape_source(url, source_name):
    response = requests.get(url, timeout=10)

    print(f"{source_name} - Status Code:", response.status_code)

    response.raise_for_status()

    soup = BeautifulSoup(response.content, "xml")
    articles = soup.find_all("item")

    news_data = []

    for article in articles[:10]:

        title_tag = article.find("title")
        link_tag = article.find("link")
        date_tag = article.find("pubDate")

        if title_tag and link_tag:

            title = title_tag.get_text(strip=True)
            link = link_tag.get_text(strip=True)

            if date_tag:
                published = date_tag.get_text(strip=True)
            else:
                published = "Not Available"

            # AI category prediction
            category = predict_category(title)

            news_data.append({
                "title": title,
                "url": link,
                "published": published,
                "source": source_name,
                "category": category
            })

    return news_data


def run_scraper():

    sources = [
        {
            "name": "BBC",
            "url": "https://feeds.bbci.co.uk/news/rss.xml"
        },
        {
            "name": "The Guardian",
            "url": "https://www.theguardian.com/world/rss"
        },
        {
            "name": "NPR",
            "url": "https://feeds.npr.org/1001/rss.xml"
        }
    ]

    # Connect to MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Heerpatel@276",
        database="news_database"
    )

    cursor = connection.cursor()

    all_news = []

    # Scrape sources
    for source in sources:

        try:

            news = scrape_source(
                source["url"],
                source["name"]
            )

            all_news.extend(news)

        except Exception as e:

            print(f"{source['name']} failed: {e}")
            print("Continuing with the next source...")

    # Insert articles
    insert_query = """
    INSERT IGNORE INTO articles
    (title, url, published, source, category)
    VALUES (%s, %s, %s, %s, %s)
    """

    new_articles = 0

    for article in all_news:

        cursor.execute(
            insert_query,
            (
                article["title"],
                article["url"],
                article["published"],
                article["source"],
                article["category"]
            )
        )

        if cursor.rowcount > 0:
            new_articles += 1

    connection.commit()

    print("\n" + "=" * 60)
    print(f"Total articles scraped: {len(all_news)}")
    print(f"New articles added to MySQL: {new_articles}")
    print("=" * 60)

    cursor.close()
    connection.close()

    print("MySQL connection closed.")


if __name__ == "__main__":
    run_scraper()