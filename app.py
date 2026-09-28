from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os
import time

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "db"),
        user=os.getenv("DB_USER", "hospital_user"),
        password=os.getenv("DB_PASSWORD", "hospital_pass"),
        database=os.getenv("DB_NAME", "hospital_db")
    )


def wait_for_db():
    for attempt in range(30):
        try:
            connection = get_db_connection()
            connection.close()
            print("MySQL database is ready.")
            return
        except mysql.connector.Error:
            print(f"Waiting for MySQL... attempt {attempt + 1}/30")
            time.sleep(2)

    raise Exception("Could not connect to MySQL database.")


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM staff ORDER BY id DESC")
    staff = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", staff=staff)


@app.route("/add", methods=["GET", "POST"])
def add_staff():
    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        department = request.form["department"]
        email = request.form["email"]
        phone = request.form["phone"]

        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            INSERT INTO staff
            (name, role, department, email, phone)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (name, role, department, email, phone)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("index"))

    return render_template("add_staff.html")


@app.route("/edit/<int:staff_id>", methods=["GET", "POST"])
def edit_staff(staff_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if request.method == "POST":
        name = request.form["name"]
        role = request.form["role"]
        department = request.form["department"]
        email = request.form["email"]
        phone = request.form["phone"]

        cursor.execute(
            """
            UPDATE staff
            SET name=%s,
                role=%s,
                department=%s,
                email=%s,
                phone=%s
            WHERE id=%s
            """,
            (name, role, department, email, phone, staff_id)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("index"))

    cursor.execute(
        "SELECT * FROM staff WHERE id=%s",
        (staff_id,)
    )

    staff = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit_staff.html", staff=staff)


@app.route("/delete/<int:staff_id>")
def delete_staff(staff_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM staff WHERE id=%s",
        (staff_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect(url_for("index"))


@app.route("/health")
def health():
    try:
        connection = get_db_connection()
        connection.close()

        return {
            "status": "healthy",
            "database": "connected"
        }, 200

    except Exception as error:
        return {
            "status": "unhealthy",
            "database": str(error)
        }, 500


if __name__ == "__main__":
    wait_for_db()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
