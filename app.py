from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "uniadventures123"
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="uniadventures"
)

print("Connected to MySQL successfully!")


@app.route("/")
def home():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trips")
    trips = cursor.fetchall()
    cursor.close()

    user_name = session.get("full_name")

    return render_template(
        "index.html",
        trips=trips,
        user_name=user_name
    )

@app.route("/book/<int:trip_id>")
def book(trip_id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM trips WHERE id = %s", (trip_id,))
    trip = cursor.fetchone()
    cursor.close()

    return render_template("booking.html", trip=trip)
@app.route("/confirm_booking/<int:trip_id>", methods=["POST"])
def confirm_booking(trip_id):
    full_name = request.form["full_name"]
    student_id = request.form["student_id"]
    phone = request.form["phone"]

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO bookings (trip_id, full_name, student_id, phone)
        VALUES (%s, %s, %s, %s)
    """, (trip_id, full_name, student_id, phone))

    db.commit()
    cursor.close()

    return render_template("success.html")
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        full_name = request.form["full_name"]
        student_id = request.form["student_id"]
        university = request.form["university"]
        university_email = request.form["university_email"]
        password = request.form["password"]

        cursor = db.cursor()

        cursor.execute("""
            INSERT INTO users
            (full_name, student_id, password, university, university_email)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            full_name,
            student_id,
            password,
            university,
            university_email
        ))

        db.commit()
        cursor.close()

        return redirect("/")

    return render_template("register.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        university_email = request.form["university_email"]
        password = request.form["password"]

        cursor = db.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM users
            WHERE university_email=%s AND password=%s
        """, (university_email, password))

        user = cursor.fetchone()
        cursor.close()

        if user:
            session["user_id"] = user["id"]
            session["full_name"] = user["full_name"]

            return redirect("/")

        return "Invalid Email or Password"

    return render_template("login.html")
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)