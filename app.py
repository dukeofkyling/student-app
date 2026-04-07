from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("PGHOST"),
        database=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        port=os.getenv("PGPORT")
    )
    return conn

@app.route("/")
def home():
    return "Student App Running on Railway!"

@app.route("/students", methods=["GET"])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students;")
    students = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify(students)

@app.route("/students", methods=["POST"])
def add_student():
    data = request.json

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO students (name, course) VALUES (%s,%s)",
        (data["name"], data["course"])
    )

    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Student added"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
