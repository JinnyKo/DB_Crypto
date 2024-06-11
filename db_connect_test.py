import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="testuser",
        password="1234",
        database="card_company"
    )


db = connect_db()
cursor = db.cursor()
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
print(tables)
cursor.close()
db.close()
