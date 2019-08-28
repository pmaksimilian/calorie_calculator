from flask import Flask, make_response, render_template, request, redirect, url_for
from models import User, db
import hashlib
import uuid


app = Flask(__name__)
db.create_all()


@app.route("/")
@app.route("/index")
def index():
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
        return render_template("index.html", title="First Page", user=user)
    else:
        return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    session_token = request.cookies.get("session_token")
    if session_token:
        user = db.query(User).filter_by(session_token=session_token).first()
        return redirect(url_for('index'), user=user)
    else:
        if request.method == "GET":
            return render_template("login.html", title="Login")
        elif request.method == "POST":
            email = request.form.get("email")
            raw_password = request.form.get("password")
            password = hashlib.sha3_256(raw_password.encode()).hexdigest()
            session_token = str(uuid.uuid4())

            user = db.query(User).filter_by(email=email).first()

            if user:
                if password == user.password:
                    response = make_response(redirect(url_for('index')))
                    response.set_cookie("session_token", session_token)
                    user.session_token = session_token
                    db.add(user)
                    db.commit()
                    return response
                else:
                    return "Wrong password, try again."
            else:
                return "Wrong email, try again."
        else:
            print("Something is wrong.")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", title="Register")
    elif request.method == "POST":
        name = request.form.get("username")
        email = request.form.get("email")
        raw_password = request.form.get("password")
        password = hashlib.sha3_256(raw_password.encode()).hexdigest()

        user = User(name=name, email=email, password=password)
        db.add(user)
        db.commit()

        return redirect(url_for('login'))
    else:
        print("Something is wrong.")


@app.route("/logout")
def logout():
    response = make_response(redirect(url_for("login")))
    response.set_cookie("session_token", "", expires=0)
    return response


if __name__ == '__main__':
    app.run(debug=True)
