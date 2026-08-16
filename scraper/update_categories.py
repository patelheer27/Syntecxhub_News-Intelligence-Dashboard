import mysql.connector
from ai_classifier import predict_category


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Heerpatel@276",
    database="news_database"
)

cursor = connection.cursor(dictionary=True)

# Get articles that don't have a category yet
cursor.execute("""
    SELECT id, title
    FROM articles
    WHERE category IS NULL
""")

articles = cursor.fetchall()

print(f"Articles without category: {len(articles)}")

update_query = """
UPDATE articles
SET category = %s
WHERE id = %s
"""

updated = 0

for article in articles:

    category = predict_category(article["title"])

    cursor.execute(
        update_query,
        (category, article["id"])
    )

    updated += 1

    print(
        f"{article['title'][:60]}... → {category}"
    )

connection.commit()

print("\n" + "=" * 50)
print(f"Articles categorized: {updated}")
print("=" * 50)

cursor.close()
connection.close()
