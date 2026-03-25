from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import re

app = Flask(__name__)

users = {
    "zeus": ["1234", ["Jemyx Orillo", 14, "Davao City", "September 2, 2026"]]
}

admin = {"admin": "admin123"}

current_user = None
current_role = None

MONTH_NAMES = {
    "january":1,"february":2,"march":3,"april":4,"may":5,"june":6,
    "july":7,"august":8,"september":9,"october":10,"november":11,"december":12
}

REAL_PLACES = {
    "davao city", "manila", "quezon city", "cebu city", "zamboanga city",
    "taguig", "antipolo", "pasig", "cagayan de oro", "parañaque",
    "dasmariñas", "valenzuela", "bacoor", "general santos", "makati",
    "san jose del monte", "caloocan", "malabon", "mandaluyong", "marikina",
    "muntinlupa", "navotas", "pasay", "san juan", "las piñas",
    "lapu-lapu city", "iligan city", "bacolod", "iloilo city", "butuan",
    "cotabato city", "tacloban", "dumaguete", "tagaytay", "baguio",
    "olongapo", "angeles city", "san fernando", "lipa city", "batangas city",
    "lucena", "naga city", "legazpi city", "puerto princesa", "koronadal",
    "pagadian", "digos", "tagum", "mati", "kidapawan", "surigao city",
    "tandag", "bislig", "bayugan", "cabadbaran", "prosperidad",
    "tangub city", "ozamiz city", "dipolog city", "dapitan", "isabela city",
    "cauayan", "santiago city", "tuguegarao", "laoag", "vigan",
    "san carlos city", "urdaneta", "dagupan", "alaminos city",
    "balanga", "malolos", "meycauayan", "cabanatuan", "tarlac city",
    "roxas city", "kalibo", "tokyo", "osaka", "kyoto", "seoul", "busan",
    "beijing", "shanghai", "hong kong", "taipei", "singapore", "bangkok",
    "jakarta", "kuala lumpur", "ho chi minh city", "hanoi", "yangon",
    "colombo", "dhaka", "karachi", "lahore", "mumbai", "delhi", "kolkata",
    "chennai", "bangalore", "hyderabad", "kathmandu", "tehran", "baghdad",
    "riyadh", "jeddah", "dubai", "abu dhabi", "doha", "kuwait city",
    "muscat", "beirut", "amman", "jerusalem", "tel aviv", "ankara", "istanbul",
    "london", "paris", "berlin", "madrid", "rome", "amsterdam", "brussels",
    "vienna", "zurich", "geneva", "stockholm", "oslo", "copenhagen",
    "helsinki", "warsaw", "prague", "budapest", "bucharest", "sofia",
    "athens", "lisbon", "dublin", "edinburgh", "manchester", "barcelona",
    "milan", "naples", "munich", "hamburg", "frankfurt", "cologne",
    "new york", "los angeles", "chicago", "houston", "phoenix", "philadelphia",
    "san antonio", "san diego", "dallas", "austin", "miami", "seattle",
    "boston", "denver", "nashville", "portland", "las vegas", "atlanta",
    "washington dc", "toronto", "montreal", "vancouver", "calgary", "ottawa",
    "mexico city", "guadalajara", "monterrey", "sao paulo", "rio de janeiro",
    "brasilia", "buenos aires", "lima", "bogota", "santiago", "caracas",
    "cairo", "lagos", "nairobi", "johannesburg", "cape town", "accra",
    "addis ababa", "dar es salaam", "kinshasa", "casablanca", "tunis",
    "sydney", "melbourne", "brisbane", "perth", "adelaide", "auckland",
    "wellington", "christchurch",
}

def is_valid_date(value):
    value = value.strip()
    parsed = None

    m = re.match(r'^([a-zA-Z]+)\s+(\d{1,2}),\s*(\d{4})$', value)
    if m:
        month_num = MONTH_NAMES.get(m.group(1).lower())
        if not month_num:
            return False
        try:
            parsed = datetime(int(m.group(3)), month_num, int(m.group(2)))
        except ValueError:
            return False

    if not parsed:
        m = re.match(r'^(\d{1,2})/(\d{1,2})/(\d{4})$', value)
        if m:
            try:
                parsed = datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))
            except ValueError:
                return False

    if not parsed:
        m = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{4})$', value)
        if m:
            try:
                parsed = datetime(int(m.group(3)), int(m.group(1)), int(m.group(2)))
            except ValueError:
                return False

    if not parsed:
        return False

    if parsed.date() < datetime.today().date():
        return False

    return True

def is_real_address(address):
    return address.strip().lower() in REAL_PLACES

def is_valid_name(name):
    return bool(re.match(r'^[a-zA-Z\s]+$', name.strip()))

def is_valid_age(age):
    return age.isdigit() and 1 <= int(age) <= 120


@app.route("/", methods=["GET", "POST"])
def login():
    global current_user, current_role

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in admin and admin[username] == password:
            current_user = username
            current_role = "admin"
            return redirect(url_for("admin_panel"))

        if username in users and users[username][0] == password:
            current_user = username
            current_role = "patient"
            return redirect(url_for("home"))

        return redirect(url_for("error"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    global users

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        name = request.form["name"].strip()
        age = request.form["age"].strip()
        address = request.form["address"].strip()

        form_data = {
            "username": username,
            "name": name,
            "age": age,
            "address": address
        }

        
        errors = {}

        if not username:
            errors["username"] = "Please fill out this field."
        elif username in users or username in admin:
            errors["username"] = "Username already taken, choose another."

        if not password:
            errors["password"] = "Please fill out this field."

        if not name:
            errors["name"] = "Please fill out this field."
        elif not is_valid_name(name):
            errors["name"] = "Full name must contain letters only."

        if not age:
            errors["age"] = "Please fill out this field."
        elif not is_valid_age(age):
            errors["age"] = "Age must be a number between 1 and 120."

        if not address:
            errors["address"] = "Please fill out this field."
        elif not is_real_address(address):
            errors["address"] = "Address not recognized. Enter a valid city (e.g. Davao City)."

        
        if errors:
            return render_template("register.html",
                errors=errors,
                form_data=form_data
            )

        users[username] = [password, [name, int(age), address, "No appointment yet"]]
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    global current_user, current_role

    if current_user is None or current_role != "patient":
        return redirect(url_for("login"))

    user_data = users[current_user][1]
    date_error = None

    if request.method == "POST":
        appointment = request.form["appointment"].strip()
        if not appointment:
            date_error = "Please enter an appointment date."
        elif not is_valid_date(appointment):
            date_error = "Please enter a valid date that is today or in the future (e.g. September 10, 2026)."
        else:
            user_data[3] = appointment

    return render_template(
        "homepage.html",
        name=user_data[0],
        age=user_data[1],
        address=user_data[2],
        appointment=user_data[3],
        date_error=date_error
    )


@app.route("/admin")
def admin_panel():
    if current_role != "admin":
        return redirect(url_for("login"))
    return render_template("adminpage.html", users=users)


@app.route("/logout")
def logout():
    global current_user, current_role
    current_user = None
    current_role = None
    return redirect(url_for("login"))


@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)