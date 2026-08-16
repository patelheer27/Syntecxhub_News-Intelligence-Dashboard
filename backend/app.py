from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Heerpatel@276",
        database="news_database"
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
    app.run(debug=True, port=5000)