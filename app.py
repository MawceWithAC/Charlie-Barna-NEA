from flask import Flask, render_template, request
from os import urandom
from flask_caching import Cache
app = Flask(__name__)
app.config["SECRET_KEY"] = "Tesst"
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300000 # timeout in seconds
user = "John Doe"
cache = Cache(app)

class User:
    User = ""
    Pass = ""
    Preliverages = "User"
    def __init__(self, UserName: str = "John Doe", Password: str = "Password"):
        self.User = UserName
        self.Pass = Password

TestUsers = [
    User("admin","Testing" ),
    User("user","Testing")

]



@app.route('/')
def onload():  # put application's code here
    cache.set("Loaded", True)

    username = cache.get("username")
    if username is None:
        cache.set("username", "")
    return app.redirect("/home",302)
@app.route("/home")
def homepage():
    usernameToShow = cache.get("username")
    if usernameToShow is None:
        usernameToShow = ""
    return render_template("Home.html", User = usernameToShow.title())


@ app.route("/login")
def loginpage():
    if cache.get("loginAttempts") is None:
        cache.set("loginAttempts", "0")

    #cache.set("username", "John Doe")
    return render_template("Login.html")

@ app.route("/CheckLogin", methods=["POST"])
def CheckLogin():
    if request.method == "POST":
        #print(request.args)
        User = request.form.get("username").lower()
        Pass = request.form.get("password")
        #print(User,Pass)
        for i in TestUsers:
            if User == i.User:
                if Pass == i.Pass:
                    cache.set("username", i.User)
                    #print("LoggedIn")
                    return app.redirect("/home", 302)
    return app.redirect("/login",302)

@app.route("/LogOut")
def LogOut():
    cache.set("username", None)
    return app.redirect("/home",302)


if __name__ == '__main__':
    app.run()
