import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Heerpatel@276",
    database="news_database"
)

print("MySQL connection successful!")

connection.close()