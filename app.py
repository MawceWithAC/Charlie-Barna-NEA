import flask
from datetime import timedelta
from Database import DatabaseHandler
from flask import Flask, render_template, request,flash,session
"""
Shows Frontend Of The Page And Sends Requests to DatabaseHandler.py
"""
app = Flask(__name__, template_folder="templates", static_folder="templates/static")
#app.register_blueprint(core, url_prefix='')
app.config["SECRET_KEY"] = "mAWCEeLL"
app.config["CACHE_TYPE"] = "SimpleCache"
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
user = "John Doe"

@app.route('/')
def onload():
    """
    Gives the user an ID

    :return: Redirect To Home
    """
    UserID = request.cookies.get('id')
    if UserID is None:
        session["id"] = 0
    
    return app.redirect("/home",302)

@app.route("/home")
def homepage():
    """
    Home Page

    :return: Render Template For Home
    """
    #flash("Testing")
    try:
        userId = session["id"]
    except:

        return flask.redirect("/", 302)
    if userId is None:
        flask.redirect("/",302)
    UserNameToShow = ""
    if userId != 0:
        UserNameToShow = DatabaseHandler.GetUserByID(userId)[1]

    return render_template("Home.html",
                            User = UserNameToShow.title(),
                            ID = userId,
                            Username = DatabaseHandler.GetUsernameFromID(userId),
                            HomeData =DatabaseHandler.GetMostPopularPosts(40))



@ app.route("/login/")
def loginpageNoFollow():
    """
    Loads Login Page
    :return: Render Template For Login
    """
  

    return render_template("Login.html",ID = 0,Follow = "home" )

@ app.route("/login/<FollowAddress>")
def loginPageWithFollow(FollowAddress):
    """
    Part One of an Overly Complicated Process
    To allow users to return to pages after login
    :param FollowAddress:
    :return: Render Template For Login
    """
    return render_template("Login.html",ID = 0,Follow = FollowAddress )

@ app.route("/login/<FollowAddress>/<Follow2>")
def loginPageWithDoubleFollow(FollowAddress,Follow2):
    """
    Part Two of an Overly Complicated Process
    To allow users to return to pages after login
    :param FollowAddress:
    :param Follow2:
    :return: Render Template For Login
    """
    return render_template("Login.html",ID = 0,Follow = f"{FollowAddress}/{Follow2}" )

@ app.route("/CheckLogin/<FollowAddress>", methods=["POST"])
def CheckLoginWithOneLink(FollowAddress):
    """
    Part Three of an Overly Complicated Process
    To allow users to return to pages after login
    :param FollowAddress:
    :return: Redirect to Login OR Redirect to last page
    """
    if request.method == "POST":
        #print(request.args)
        User = DatabaseHandler.VerifyLogin(request.form.get("username").lower().strip())
        Pass = DatabaseHandler.VerifyLogin(request.form.get("password").strip())
        return CheckLogin(User, Pass,FollowAddress)
    return app.redirect(f"/login/{FollowAddress}", 302)


@ app.route("/CheckLogin/<FollowAddress>/<Address2>", methods=["POST"])
def CheckLoginWithTwoLink(FollowAddress,Address2):
    """
    Part Three of an Overly Complicated Process
    To allow users to return to pages after login
    :param FollowAddress:
    :return: Redirect to Login OR Redirect to last page
    """
    if request.method == "POST":
        #print(request.args)
        User = DatabaseHandler.VerifyLogin(request.form.get("username").lower().strip())
        Pass = DatabaseHandler.VerifyLogin(request.form.get("password").strip())
        return CheckLogin(User, Pass,f"{FollowAddress}/{Address2}")
    return app.redirect("/login", 302)

def CheckLogin(User, Pass,FollowAddress):
    """
    Checks the Login of the user and returns a redirect to Login
    or sends them back to their last page, If None Then Home
    :param User:
    :param Pass:
    :param FollowAddress:
    :return: Redirect to last page or Login
    """
    if User is None or Pass is None:
            flash("Please Use Alphabetic Symbols or Symbols")
    else:
        LogginSucsess, LoginDetails = DatabaseHandler.CheckLogin(User,Pass)
        if LogginSucsess:
            session["id"] = LoginDetails[0]
            return app.redirect("/"+FollowAddress,302)
        else:
            flash("Wrong Username Or Password")
    return app.redirect(f"/login/{FollowAddress}", 302)


@app.route("/LogOut")
def LogOut():
    """
    Logs The User Out
    :return: Redirect Home
    """
    session["id"] = 0
    return app.redirect("/home",302)
@app.route("/createaccount/")
def CreateAccountNoFollow():
    """
    Long way to create account, Same as Login
    :return: render template for login
    """
    return render_template("CreateAccount.html",ID = 0)
@app.route("/createaccount/<Follow1>")
def CreateAccountOneFollow(Follow1):
    """
    Long way to create account, Same as Login
    :return: render template for login
    """
    return render_template("CreateAccount.html",ID = 0, Follow = Follow1)
@app.route("/createaccount/<Follow1>/<Follow2>")
def CreateAccountTwoFollow(Follow1,Follow2):
    """
    Long way to create account, Same as Login
    :return: render template for login
    """
    return render_template("CreateAccount.html",ID = 0, Follow = f"{Follow1}/{Follow2}")

@app.route("/users/<user>")
def ShowUser(user):
    """
    Checks if a user exists and if it does then displays it
    :param user:
    :return: Render Tempalte For User
    """
    try:
        Id = session["id"]
    except:
        Id = None
    userData = DatabaseHandler.GetPostsFromUser(user)
    userID = DatabaseHandler.GetIdFromUsername(user)
    ExcersiseLists = DatabaseHandler.GetExcersiseLists(int(userID))
    if userID is None:
        return app.redirect("/home",302)

    return render_template("User.html",ID = Id,
                           Username=DatabaseHandler.GetUsernameFromID(Id),
                           UserName = user,
                            data = userData,
                           exList=ExcersiseLists
                            )




@app.route("/post/<post>")
def ShowPost(post):
    """
    Page for a post
    :param post:
    :return: render template for Post
    """
    PostData = DatabaseHandler.GetPost(int(post))
    CommentData = DatabaseHandler.GetComments(int(post))
    #print(CommentData)
    if PostData is None:
        return app.redirect("/home",302)
    try:
        Id = session["id"]
    except:
        Id = None
    if Id is None:
        session["id"] = 0
        Id = 0
    return render_template("Post.html",ID = Id,
                            data = PostData,
                            Comments = CommentData,
                            PostID = post
                            )



@app.route("/exercise/<ExId>")
def ShowExersise(ExId):
    """
    Page which contains the excersise data nad posts
    :param ExId:
    :return: Render Template For Post
    """
    try:
        Id = session["id"]
    except:
        Id = None
    if Id is None:
        Id = 0
        session["id"] = 0
    return render_template("excersise.html",ID = Id,
                           Username=DatabaseHandler.GetUsernameFromID(Id),
                            ExcersiseData= DatabaseHandler.GetExcersiseData(ExId),
                            Data = DatabaseHandler.GetPostsFromExcersise(ExId)
                            )
@app.route("/exercise/<ExId>/search", methods = ["GET"])
def ExcersiseSearch(ExId):
    """
    Search bar In the Excersise Page
    :param ExId:
    :return: render template with the data from the search
    """
    SearchInput = request.args.get('Search')
    try:
        Id = session["id"]
    except:
        Id = None
    if SearchInput is None or SearchInput == "":
        SearchDefault = ""
        return flask.redirect(f"/exercise/{ExId}",302)
    else:
        SearchData = DatabaseHandler.SearchPosts(SearchInput,ExId)
        SearchDefault = str(SearchInput)
    #print(Data)
    return render_template("excersise.html",ID = Id,
                           Username=DatabaseHandler.GetUsernameFromID(Id),
                            ExcersiseData= DatabaseHandler.GetExcersiseData(ExId),
                            ExSearchInput = SearchDefault,
                            Data = SearchData)

@app.route("/likepost", methods = ["POST"])
def LikePost():
    """
    Sends a request to the database to like a post
    :return: Html Status (Json)
    """
    if request.method == "POST":
        try:
            Request = request.json
            print(Request)
            DatabaseHandler.AddLike(Request['UserId'],Request['PostId'],Request['LikeValue'])
        except Exception as e:
            #print(e)
            print(f"ERROR: {e}")
        return {'status': 'success', "code": 202}

@app.route("/getLikes", methods = ["GET"])
def GetLikes():
    """
    Requests to get the current likes on the post
    :return: Html Status (Json)
    """
    if request.method == "GET":
        Id = request.args.get('ID')
        print(Id)
        Likes = DatabaseHandler.GetLikes(int(Id))
        return {"code": 200, "Likes":Likes[0], "Dislikes":Likes[1]}

@app.route("/CreateAccountCheck", methods = ["POST"])
def CreateAccountCheck():
    """
    Complicated Way To Create an account
    and have the user return, See Login
    :return: Create Account
    """
    if request.method == "POST":
        Name = DatabaseHandler.CheckName(request.form.get("Name").lower().strip())
        User = DatabaseHandler.VerifyLogin(request.form.get("username").lower().strip())
        Pass = DatabaseHandler.VerifyLogin(request.form.get("password").strip())
        Pass2 = request.form.get("password2").strip()
        return CreateAccount(Name,User,Pass,Pass2,"home")




@app.route("/CreateAccountCheck/<Follow1>", methods = ["POST"])
def CreateAccountCheckOneFollow(Follow1):
    """
    Complicated Way To Create an account
    and have the user return, See Login
    :return: Create Account
    """
    if request.method == "POST":
        Name = DatabaseHandler.CheckName(request.form.get("Name").lower().strip())
        User = DatabaseHandler.VerifyLogin(request.form.get("username").lower().strip())
        Pass = DatabaseHandler.VerifyLogin(request.form.get("password").strip())
        Pass2 = request.form.get("password2").strip()
        return CreateAccount(Name,User,Pass,Pass2,Follow1)
        #return app.redirect(f"/createaccount/{Follow1}", 400)

@app.route("/CreateAccountCheck/<Follow1>/<Follow2>", methods = ["POST"])
def CreateAccountCheckTwoFollow(Follow1,Follow2):
    """
    Complicated Way To Create an account
    and have the user return, See Login
    :return: Create Account
    """
    if request.method == "POST":
        Name = DatabaseHandler.CheckName(request.form.get("Name").lower().strip())
        User = DatabaseHandler.VerifyLogin(request.form.get("username").lower().strip())
        Pass = DatabaseHandler.VerifyLogin(request.form.get("password").strip())
        Pass2 = request.form.get("password2").strip()
        return CreateAccount(Name,User,Pass,Pass2,f"{Follow1}/{Follow2}")

@app.route("/CommentOnPost", methods = ["POST"])
def AddComment():
    """
    Adds A Comment To The Database
    Comments are regular posts with a "Parent" Attached
    :return: Html Status (Json)
    """
    if request.method == "POST":
        try:
            Request = request.json
            print(Request)
            DatabaseHandler.CreateComment([Request['Comment'],Request['User'],Request['ParentID']])

        except Exception as e:
            #print(e)
            print(f"ERROR: {e}")
            return {'status': 'error', "code": 500}
        return {'status': 'success', "code": 202}

@app.route("/search", methods = ["GET"])
def SearchPage():
    """
    Shows the Search Page When Somebody presses enter on the search bar
    :return: Render template for search
    """
    SearchInput = request.args.get('Search')
    try:
        Id = session["id"]
    except:
        Id = None
    if SearchInput is None or SearchInput == "":
        SearchDefault = ""
        return flask.redirect("/home",302)
    else:
        SearchData = DatabaseHandler.SearchPosts(SearchInput)
        Ex = DatabaseHandler.SearchExcersises(SearchInput)
        SearchDefault = str(SearchInput)


    #print(Data)
    return render_template("Search.html",
                           ID = Id,
                           SearchInput = SearchDefault,
                           Data = SearchData,
                           ExData = Ex,
                           Username=DatabaseHandler.GetUsernameFromID(Id)
                            )


def CreateAccount(Name,User,Pass,Pass2,Follow):
    """
    Creates an account,
    Very Bad Way to implement but no time to fix
    :param Name:
    :param User:
    :param Pass:
    :param Pass2:
    :param Follow:
    """
    if Name is None or User is None or Pass is None:
        flash("Please Use Alphabetic Symbols or Symbols")
    else:
        if Pass != Pass2:
            flash("Both Passwords Must Be The Same")
        else:
            AddAccount = DatabaseHandler.AddUserToDatabase([Name,User,Pass])
            if AddAccount == 201:
                flash("Sucsesfully Created Account")
                return app.redirect(f"/login/{Follow}",302)
            elif AddAccount == 409:
                flash("UserName Already Taken!")


    return app.redirect(f"/createaccount/{Follow}",302)
    #return app.redirect(f"/createaccount/{Follow1}/{Follow2}", 400)

@app.route("/newpost/<default>", methods = ["GET"])
def NewPostPageWithDefault(default):
    """
    Shows a page for a new post, Takes a Excersise as a peramater
    :param default:
    :return: Render Tempalte For A New Post
    """
    try:
        Id = session["id"]
    except:
        Id = None
    if Id is None or Id == 0:
        return app.redirect(f"/login/newpost/{default}")
    #print(Data)
    Data = DatabaseHandler.GetAllExcersises()
    try:
        newDefault = int(default)
    except:
        return app.redirect("/Home")
    #print(Ex)
    return render_template("NewPost.html",
                           Username=DatabaseHandler.GetUsernameFromID(Id),
                           ID = Id
                           ,Data = Data,
                            Default = default
                            )


@app.route("/newpost", methods = ["GET"])
def NewPostPage():
    """
    Shows a page for a new post
    :return:
    """
    try:
        Id = session["id"]
    except:
        Id = None
    if Id is None or Id == 0:
        return app.redirect("/login/newpost")
    #print(Data)
    Data = DatabaseHandler.GetAllExcersises()

    #print(Ex)
    return render_template("NewPost.html",
                           ID = Id
                           ,Data = Data,
                           Default = 0,
    Username = DatabaseHandler.GetUsernameFromID(Id)
                            )

@app.route("/CreatePost", methods = ["POST"])
def CreatePost():
    """
    Creates a post takes data from a POST Request
    :return: Redirect To New Post Or To itself On an Error
    """
    if request.method == "POST":
        try:
            Request = request.form
            #print("Request:",Request)
            try:
                Id = session["id"]
            except:
                Id = None
            NewPostID = DatabaseHandler.CreatePost([Request["description"],
                                        int( Request["excersise"] ),
                                        int(Id),Request["title"]])
            if NewPostID is None:
                return app.redirect("NewPost",302)
            else:
                return app.redirect(f"/post/{NewPostID}", 302)

        except:
            print("ERROR")
    return app.redirect("/home",302)

@app.route("/CreateExcersise", methods = ["POST"])
def CreateExcersise():
    """
    Post Request TO Create An Excersise
    :return: Redirect To New Post Or To itself On an Error
    """
    if request.method == "POST":
        try:
            Request = request.form
            #print(Request,int(Request.get("MuscleID")),Request.get("Name"))
            NewExID = None
            if request is not None:
                NewExID = DatabaseHandler.CreateExcerise(int(Request.get("MuscleID")),Request.get("Name") )
            if NewExID is None:
                return app.redirect("NewPost",302)
            else:
                return app.redirect(f"/exercise/{NewExID}", 302)

        except Exception as e:
            print("ERROR:",e)
    return app.redirect("/home",302)

@app.route("/newexcersise")
def newExcersise():
    """
    Shows the page where a user can create a new excersise
    :return: Render template for newexcersise
    """
    ExInput = request.args.get('Default')
    if ExInput == None or ExInput == "":
        data = ""
    else:
        data = ExInput
    try:
        Id = session["id"]
    except:
        Id = None
    if Id is None or Id == 0:
        return app.redirect(f"/login/newexcersise?Default={ExInput}")
    return render_template("CreateExcersise.html",
                           Username=DatabaseHandler.GetUsernameFromID(Id),
                           ID = Id,
                           ExInput = data,
                           Default = 0
                            )
@app.route("/CreateExcersiseList")
def excersiseListCreation():
    """
    Renamed to routine later on
    Shows Page to create a excersise routine
    :return: Render Template for routine or redirect to a login
    """
    try:
        Id = session["id"]
    except:
        Id = None
    if Id is None or Id == 0:
        return app.redirect("/login/CreateExcersiseList")
    #print(Data)

    #print(Ex)
    return render_template("CreateExcersiseList.html",
                           ID = Id,
    Username = DatabaseHandler.GetUsernameFromID(Id),
                           Data = DatabaseHandler.GetAllExcersises()
                            )
@app.route("/CreateExcersiseListServer", methods = ["POST"])
def CreateExcersiseListOnServer():
    """
    Creaets An Excersise List On The Server
    :return: Html Code (Json)
    """
    if request.method == "POST":
        try:
            Request = request.json
            print(Request)
            DatabaseHandler.CreateList(Request)
            #print("Request:",Request)

        except Exception as E:
            print("ERROR:",E)
    return {'status': 'success', "code": 202}

if __name__ == '__main__':
    #app.run(host = "0.0.0.0")
    app.run()