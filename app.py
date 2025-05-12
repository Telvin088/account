from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "telvinmaina"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# create database models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    profile_image = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(120), nullable=False)

    # one to one relationship with account
    account = db.relationship("Account", backref="user", uselist=False)


class Account(db.Model):
    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    followers = db.Column(db.Integer)
    messages = db.Column(db.String(250))

    # foreign key to link to user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    links = db.Column(db.String(120))
    image = db.Column(
        db.String(250)
    )  # Specify a suitable data type for the image column
    likes = db.Column(db.Integer)
    saves = db.Column(db.Integer)
    comments = db.Column(db.String(120))
    tags = db.Column(db.String(120))

    # foreign key to link to user
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # relationship to access the user who created the post
    user = db.relationship("User", backref="post")


# routes
@app.route("/signup", methods=["POST", "GET"])
def signup():
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


@app.route("/account", methods=["POST", "GET"])
def account():
    return render_template("account.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    return render_template("logout.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
