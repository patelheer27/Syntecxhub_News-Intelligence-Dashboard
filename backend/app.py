from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST", "localhost"),
        port=int(os.environ.get("MYSQLPORT", "3306")),
        user=os.environ.get("MYSQLUSER", "root"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE", "news_database")
    )


@app.route("/")
def home():
    return jsonify({
        "message": "News Intelligence API is running"
    })


@app.route("/api/news")
def get_news():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT id, title, url, published, source, category, scraped_at
    FROM articles
    ORDER BY scraped_at DESC
    """

    cursor.execute(query)

    news = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(news)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

