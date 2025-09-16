
from Database import DatabaseHandler

from flask import Flask, render_template, request,flash
#from os import urandom
from flask_caching import Cache

app = Flask(__name__)
app.config["SECRET_KEY"] = "mAWCEeLL"
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300000 # timeout in seconds
user = "John Doe"
cache = Cache(app)

class UserClass:
    User = ""
    Pass = ""
    perliverages = "User"
    def __init__(self, UserName: str = "John Doe", Password: str = "Password"):
        self.User = UserName
        self.Pass = Password

TestUsers = [
    UserClass("admin","Testing" ),
    UserClass("user","Testing")

]

@app.route('/')
def onload():  # put application's code here
    cache.set("Loaded", True)

    UserID = cache.get("id")
    if UserID is None:
        cache.set("id", 0)
    
    return app.redirect("/home",302)
@app.route("/home")
def homepage():
    flash("Testing")
    userId = cache.get("id")
    UserNameToShow = ""
    if userId is None:
        return app.redirect("/",302)
    if userId != 0:
        UserNameToShow = DatabaseHandler.GetUserByID(userId)[1]
    return render_template("Home.html", User = UserNameToShow.title(),ID = userId)


@ app.route("/login")
def loginpage():

    #cache.set("username", "John Doe")
    return render_template("Login.html")

@ app.route("/CheckLogin", methods=["POST"])
def CheckLogin():
    if request.method == "POST":
        #print(request.args)
        User = request.form.get("username")
        Pass = request.form.get("password")
        #print(User,Pass)
#         for i in TestUsers:
#             if User == i.User:
#                 if Pass == i.Pass:
#                     cache.set("username", i.User)
#                     #print("LoggedIn")
#                     return app.redirect("/home", 302)
        
        LogginSucsess, LoginDetails = DatabaseHandler.CheckLogin(User,Pass)
        if LogginSucsess:
            cache.set("id", LoginDetails[0])
            return app.redirect("/home",302)
    return app.redirect("/login",302)

@app.route("/LogOut")
def LogOut():
    cache.clear()
    return app.redirect("/home",302)
@app.route("/createaccount")
def CreateAccount():
    return render_template("CreateAccount.html")
@app.route("/CreateAccountCheck", methods = ["POST"])
def CreateAccountCheck():
    if request.method == "POST":
        Name = request.form.get("Name").lower()
        User = request.form.get("username").lower()
        Pass = request.form.get("password")
        Pass2 = request.form.get("password2")
        if Pass != Pass2:
            flash("Both Passwords Must Be The Same")
        else:
            AddAccount = DatabaseHandler.AddUserToDatabase([Name,User,Pass])
            if AddAccount == 201:
                flash("Sucsesfully Created Account")
                return app.redirect("/login",302)
            elif AddAccount == 409:
                flash("UserName Already Taken!")


        return app.redirect("/createaccount",302)

    return app.redirect("/createaccount",400)

if __name__ == '__main__':
    app.run()
