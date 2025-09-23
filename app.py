
from Database import DatabaseHandler

from flask import Flask, render_template, request,flash,Blueprint
import os
from flask_caching import Cache


#print(TEMPLATE_DIR,":",STATIC_DIR)
app = Flask(__name__, template_folder="templates", static_folder="templates/static")
#app.register_blueprint(core, url_prefix='')
app.config["SECRET_KEY"] = "mAWCEeLL"
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300000 # timeout in seconds
user = "John Doe"
cache = Cache(app)




# Ensure responses aren't cached
@app.after_request
def after_request(response):
    
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate,public, max-age=0"
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.cache_control.max_age = 0
    return response


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
    #flash("Testing")
    userId = cache.get("id")
    UserNameToShow = ""
    if userId is None:
        return app.redirect("/",302)
    if userId != 0:
        UserNameToShow = DatabaseHandler.GetUserByID(userId)[1]
    return render_template("Home.html",
                           User = UserNameToShow.title(),
                           ID = userId,
                           Username = DatabaseHandler.GetUsernameFromID(userId),
                           HomeData =DatabaseHandler.GetMostPopularPosts(10))


@ app.route("/login")
def loginpage():
    
    #cache.set("username", "John Doe")
    return render_template("Login.html",ID = 0, )

@ app.route("/CheckLogin", methods=["POST"])
def CheckLogin():
    if request.method == "POST":
        #print(request.args)
        User = DatabaseHandler.StopSQlnjection(request.form.get("username"))
        Pass = DatabaseHandler.StopSQlnjection(request.form.get("password"))
        
        #print(User,Pass)
#         for i in TestUsers:
#             if User == i.User:
#                 if Pass == i.Pass:
#                     cache.set("username", i.User)
#                     #print("LoggedIn")
#                     return app.redirect("/home", 302)
        if User is None or Pass is None:
            flash("Please Use Valid Inputs")
        else:
            LogginSucsess, LoginDetails = DatabaseHandler.CheckLogin(User,Pass)
            if LogginSucsess:
                cache.set("id", LoginDetails[0])
                return app.redirect("/home",302)
            else:
                flash("Wrong Username Or Password")
    return app.redirect("/login",302)

@app.route("/LogOut")
def LogOut():
    cache.clear()
    return app.redirect("/home",302)
@app.route("/createaccount")
def CreateAccount():
    return render_template("CreateAccount.html",ID = 0)

@app.route("/users/<user>")
def ShowUser(user):
    print(user)
    return app.redirect("/home",302)

@app.route("/post/<post>")
def ShowPost(post):
    print(post)
    return app.redirect("/home",302)
@app.route("/exercise/<ExId>")
def ShowExersise(ExId):
    #print(DatabaseHandler.GetExcersiseData(id))
    Id = cache.get("id")
    if Id == None:
        Id = 0
        cache.set("id",0)
    return render_template("excersise.html",ID = Id,
                           Username = DatabaseHandler.GetUsernameFromID(Id),
                           Data = DatabaseHandler.GetPostsFromExcersise(ExId)
                           )
@app.route("/accountsettings")
def GetSettings():
    #response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    Id = cache.get("id")
    if Id is None or Id == 0:
        return app.redirect("/login", 302)
    else:
        return render_template("accountsettings.html",
                               ID = Id,
                           )
        
@app.route("/CreateAccountCheck", methods = ["POST"])
def CreateAccountCheck():
    if request.method == "POST":
        Name = DatabaseHandler.StopSQlnjection(request.form.get("Name").lower())
        User = DatabaseHandler.StopSQlnjection(request.form.get("username").lower())
        Pass = DatabaseHandler.StopSQlnjection(request.form.get("password"))
        Pass2 = request.form.get("password2")
        if Name is None or User is None or Pass is None:
            flash("Please Do Not Use The Character -")
        else:
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
