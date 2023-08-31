from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from db.connection import *
from helpers.passwordPolicies import *

app = Flask(__name__)

# strong secret key => prevent brute-forcing & cookies attacks
app.config["SECRET_KEY"] = "sahdgjkshgdjkhsakjdhkasjhdkj"

# rate limiter =>
# to prevent brute-forcing attack on specific routes that
# attacker can attack on it
limiter = Limiter(
    get_remote_address, app=app, default_limits=["150 per day", "70 per hour"]
)


@app.route("/")
def home():
    if "username" not in session:
        flash("You're not logged in!!", "danger")
        return redirect(url_for("login"))
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
@limiter.limit("5 per minute")
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]

        user = get_user_by_username(username)

        if user:
            if is_password_matched(password, user[3]):
                session["username"] = user[1]
                session["user_id"] = user[0]
                return redirect(url_for("home"))

        flash("Invalid Credentials!", "danger")
        return render_template("login.html")


@app.route("/sign-up", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        username = request.form["username"]
        password = request.form["password1"]
        email = request.form["email"]
        confirmPassword = request.form["password2"]

        user = get_user_by_username(username)

        if user:
            flash("Username already exists!", "danger")
            return render_template("register.html")

        if password != confirmPassword:
            flash("Password doesn't match!!", "warning")
            return render_template("register.html")

        if check_password_policies(password):
            add_user(username, password, email)
            flash("Username is registered Successfully!", "success")
        else:
            flash("Your password is weak try another strong one!", "warning")
            return render_template("register.html")

    return redirect(url_for("login"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
