from flask import Flask, make_response, render_template, request, redirect, url_for
from models import User, db, Data
import hashlib
import uuid
from sqlalchemy import exc
from foods import macro_calculator, mealplan_calculator


app = Flask(__name__)
db.create_all()


# funkcije v common directory (obvezno dodaj __init__)
# checks if user is logged in
def check_login():
    session_token = request.cookies.get("session_token")
    user = db.query(User).filter_by(session_token=session_token).first()
    return user


# logs the user in
def log_in(user):
    session_token = str(uuid.uuid4())
    response = make_response(redirect(url_for('index')))
    response.set_cookie("session_token", session_token)
    user.session_token = session_token
    db.add(user)
    db.commit()
    return response


# renders the first page, which is a little different if user is logged in or not
@app.route("/")
@app.route("/index")
def index():
    user = check_login()
    if user:
        return render_template("index.html", title="First Page", user=user)
    else:
        return render_template("index.html", title="First Page")


# 3 options: redirect logged in users to index, render a login page or log in a user
@app.route("/login", methods=["GET", "POST"])
def login():
    user = check_login()
    if user:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("login.html", title="Login")
    elif request.method == "POST":
        email = request.form.get("email")
        raw_password = request.form.get("password")
        password = hashlib.sha3_256(raw_password.encode()).hexdigest()

        user = db.query(User).filter_by(email=email).first()

        if user:
            if password == user.password:
                return log_in(user)
            else:
                return render_template("login.html", title="Login", wrong_password=True)
        else:
            return render_template("login.html", title="Login", wrong_email=True)
    else:
        print("Something is wrong.")


# register new users
@app.route("/register", methods=["GET", "POST"])
def register():
    user = check_login()
    if user:
        return redirect(url_for('index'))
    if request.method == "GET":
        return render_template("register.html", title="Register")
    elif request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        raw_password = request.form.get("password")
        raw_password2 = request.form.get("passwordConf")

        if raw_password != raw_password2:
            return render_template("register.html", title="Register", diffPass=True)

        password = hashlib.sha3_256(raw_password.encode()).hexdigest()

        user = User(name=name, email=email, password=password)
        try:
            db.add(user)
            db.commit()
        except exc.IntegrityError:
            return render_template("register.html", title="Register", message=True)

        return log_in(user)
    else:
        return "Something is wrong."


# simple logout by deleting cookie
@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("index")))
    response.set_cookie("session_token", "", expires=0)
    return response


@app.route("/calculator", methods=["POST", "GET"])
def calculator():
    user = check_login()
    if not user:
        return redirect(url_for('login'))
    if request.method == "GET":
        return render_template("calculator.html", title="Calculator", user=user)
    elif request.method == "POST":
        sex = request.form.get("sex")
        weight = int(request.form.get("weight"))
        height = int(request.form.get("height"))
        age = int(request.form.get("age"))
        activity = float(request.form.get("activity"))
        goals = int(request.form.get("goals"))

        # gets data from form and calculate results using the Mufflin equation

        if sex == "male":
            resting_energy_expenditure = (10 * weight) + (6.25 * height) - (5 * age) + 5
            total_energy_expenditure = resting_energy_expenditure * activity
        else:
            resting_energy_expenditure = (10 * weight) + (6.25 * height) - (5 * age) - 161
            total_energy_expenditure = resting_energy_expenditure * activity

        calorie_intake = int(total_energy_expenditure)

        if goals == 2:
            calorie_intake -= 500
        elif goals == 3:
            calorie_intake -= 1000
        elif goals == 4:
            calorie_intake += 500
        elif goals == 5:
            calorie_intake += 1000

        # check if calculation already exists
        calorie_data = db.query(Data).filter_by(user_id=user.id).first()
        if calorie_data:
            calorie_data.calories = calorie_intake
            calorie_data.weight = weight
            calorie_data.goals = goals
        else:
            calorie_data = Data(calories=calorie_intake, weight=weight, goals=goals, user_id=user.id)
        db.add(calorie_data)
        db.commit()
        return redirect(url_for("my_profile"))

    else:
        return "Something is wrong."


# render page with results
@app.route("/my-profile")
def my_profile():
    user = check_login()
    if not user:
        return redirect(url_for('login'))

    breakfast = {
        "oatmeal": 40,
        "yogurt": 50,
        "almonds": 5,
        "whey": 15
    }
    brunch = {
        "eggs": 2,
        "wholemeal bread": 40
    }
    lunch = {
        "chicken breast": 120,
        "rice": 35
    }
    dinner = {
        "salmon": 90,
        "potato": 110
    }
    calorie_data = db.query(Data).filter_by(user_id=user.id).first()
    breakfast = mealplan_calculator(calorie_data.calories, breakfast)
    brunch = mealplan_calculator(calorie_data.calories, brunch)
    lunch = mealplan_calculator(calorie_data.calories, lunch)
    dinner = mealplan_calculator(calorie_data.calories, dinner)

    macros = macro_calculator(calorie_data.calories)

    return render_template("my_profile.html", title="My Profile", calorie_data=calorie_data, macros=macros, user=user,
                           breakfast=breakfast, brunch=brunch, lunch=lunch, dinner=dinner)


#
# NASLEDNJIC!!!
# - uredi izpis dnevnega jedilnika in nasploh my-profile strani
# - nato zrihtaj migracijo baze in foreign-key
# - formula za izračuna jedilnika
#


if __name__ == '__main__':
    app.run(debug=True)
