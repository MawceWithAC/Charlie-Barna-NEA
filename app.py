from asyncio import run as ARun
import quart
from Database import DatabaseHandler
from flask_caching import Cache
from quart import Quart, render_template, request,flash,Blueprint
import os


#[sublist[1] for sublist in newList] Get Every Second in a 2d array

#print(TEMPLATE_DIR,":",STATIC_DIR)
app = Quart(__name__, template_folder="templates", static_folder="templates/static")
#app.register_blueprint(core, url_prefix='')
app.config["SECRET_KEY"] = "mAWCEeLL"
app.config["CACHE_TYPE"] = "SimpleCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300000 # timeout in seconds
user = "John Doe"
cache = Cache(app)

async def FlashUser(Message: str = ""):
    await flash(Message)


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
async def onload():  # put application's code here
    cache.set("Loaded", True)

    UserID = cache.get("id")
    if UserID is None:
        cache.set("id", 0)
    
    return app.redirect("/home",302)
@app.route("/home")
async def homepage():
    #ARun(FlashUser("Testing"))
    userId = cache.get("id")
    UserNameToShow = ""
    if userId is None:
        return app.redirect("/",302)
    if userId != 0:
        UserNameToShow = DatabaseHandler.GetUserByID(userId)[1]
    return await render_template("Home.html",
                           User = UserNameToShow.title(),
                           ID = userId,
                           Username = DatabaseHandler.GetUsernameFromID(userId),
                           HomeData =DatabaseHandler.GetMostPopularPosts(10))



@ app.route("/login/")
async def loginpageNoFollow():
    #cache.set("username", "John Doe")

    return await render_template("Login.html",ID = 0,Follow = "home" )

@ app.route("/login/<FollowAddress>")
async def loginPageWithFollow(FollowAddress):
    #cache.set("username", "John Doe")
    print(FollowAddress)
    return await render_template("Login.html",ID = 0,Follow = FollowAddress )

@ app.route("/login/<FollowAddress>/<Follow2>")
async def loginPageWithDoubleFollow(FollowAddress,Follow2):
    #cache.set("username", "John Doe")
    print(FollowAddress)
    return await render_template("Login.html",ID = 0,Follow = f"{FollowAddress}/{Follow2}" )

@ app.route("/CheckLogin/<FollowAddress>", methods=["POST"])
def CheckLoginWithOneLink(FollowAddress):
    async def GetRequest(Form):
        x= (await request.form).get(Form)
        return x
    print(FollowAddress)
    
    if request.method == "POST":
        #print(request.args)
        User = DatabaseHandler.VerifyLogin(ARun(GetRequest("username")).lower().strip())
        Pass = DatabaseHandler.VerifyLogin(ARun(GetRequest("password")).strip())
        return CheckLogin(User, Pass,FollowAddress)
    return app.redirect(f"/login/{FollowAddress}", 302)


@ app.route("/CheckLogin/<FollowAddress>/<Address2>", methods=["POST"])
async def CheckLoginWithTwoLink(FollowAddress,Address2):
    async def GetRequest(Form):
        x= (await request.form).get(Form)
        return x
    print(FollowAddress)
    
    if request.method == "POST":
        #print(request.args)
        User = DatabaseHandler.VerifyLogin(ARun(GetRequest("username")).lower().strip())
        Pass = DatabaseHandler.VerifyLogin(ARun(GetRequest("password")).strip())
    return app.redirect("/login", 302)

def CheckLogin(User, Pass,FollowAddress):
    print("checking",User)
    if User is None or Pass is None:
            ARun(FlashUser("Please Use Alphabetic Symbols or Symbols"))
    else:
        LogginSucsess, LoginDetails = DatabaseHandler.CheckLogin(User,Pass)
        if LogginSucsess:
            cache.set("id", LoginDetails[0])
            return app.redirect("/"+FollowAddress,302)
        else:
            ARun(FlashUser("Wrong Username Or Password"))
    return app.redirect(f"/login/{FollowAddress}", 302)
@app.route("/LogOut")
async def LogOut():
    cache.clear()
    return app.redirect("/home",302)
@app.route("/createaccount/")
async def CreateAccountNoFollow():
    return await render_template("CreateAccount.html",ID = 0)
@app.route("/createaccount/<Follow1>")
async def CreateAccountOneFollow(Follow1):
    return await render_template("CreateAccount.html",ID = 0, Follow = Follow1)
@app.route("/createaccount/<Follow1>/<Follow2>")
async def CreateAccountTwoFollow(Follow1,Follow2):
    return await render_template("CreateAccount.html",ID = 0, Follow = f"{Follow1}/{Follow2}")

@app.route("/users/<user>")
async def ShowUser(user):
    Id = cache.get("id")
    print(user)
    testdata = [[2,"TitleName","Tester",1,0,1,"Bench Press",user,"3:00","10-9-25",-1]]
    return await render_template("User.html",ID = Id,
                           data = testdata
                           )
@app.errorhandler(404)
async def Error404(error):
    return app.redirect("/home",302)



@app.route("/post/<post>")
async def ShowPost(post):
    print(post)
    PostData = DatabaseHandler.GetPost(int(post))
    CommentData = DatabaseHandler.GetComments(int(post))
    #print(CommentData)
    if PostData is None:
        return app.redirect("/home",302)
    Id = cache.get("id")
    return await render_template("Post.html",ID = Id,
                           data = PostData,
                           Comments = CommentData
                           )



@app.route("/exercise/<ExId>")
async def ShowExersise(ExId):
    #print(DatabaseHandler.GetExcersiseData(id))
    Id = cache.get("id")
    if Id == None:
        Id = 0
        cache.set("id",0)
    return await render_template("excersise.html",ID = Id,
                           ExcersiseData= DatabaseHandler.GetExcersiseData(ExId),
                           Data = DatabaseHandler.GetPostsFromExcersise(ExId)
                           )
@app.route("/exercise/<ExId>/search", methods = ["GET"])
async def ExcersiseSearch(ExId):
    SearchInput = request.args.get('Search')
    Id = cache.get("id")
    if SearchInput is None or SearchInput == "":
        SearchDefault = ""
        return await quart.redirect(f"/exercise/{ExId}",302)
    else:
        SearchData = DatabaseHandler.SearchPosts(SearchInput,ExId)
        SearchDefault = str(SearchInput)
    #print(Data)
    return await render_template("excersise.html",ID = Id,
                           ExcersiseData= DatabaseHandler.GetExcersiseData(ExId),
                           ExSearchInput = SearchDefault,
                           Data = SearchData)


@app.route("/accountsettings")
async def GetSettings():
    #response.headers.add('Cache-Control', 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0')
    Id = cache.get("id")
    if Id is None or Id == 0:
        return app.redirect("/login", 302)
    else:
        return await render_template("accountsettings.html",
                               ID = Id,
                           )
@app.route("/likepost", methods = ["POST"])
async def LikePost():
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
async def GetLikes():
    if request.method == "GET":
        Id = request.args.get('ID')
        print(Id)
        Likes = DatabaseHandler.GetLikes(int(Id))
        return {"code": 200, "Likes":Likes[0], "Dislikes":Likes[1]}

@app.route("/CreateAccountCheck", methods = ["POST"])
def CreateAccountCheck():
    async def GetRequest(Form):
        x= (await request.form).get(Form)
        return x
    print("Creating" + ARun(GetRequest("Name")))
    if request.method == "POST":
        Name = DatabaseHandler.CheckName(ARun(GetRequest("Name")).lower().strip())
        User = DatabaseHandler.VerifyLogin(ARun(GetRequest("username")).lower().strip())
        Pass = DatabaseHandler.VerifyLogin(ARun(GetRequest("password")).strip())
        Pass2 = ARun(GetRequest("password2")).strip()
        return CreateAccount(Name,User,Pass,Pass2,"home")
        #return app.redirect("/createaccount", 400)



@app.route("/CreateAccountCheck/<Follow1>", methods = ["POST"])
def CreateAccountCheckOneFollow(Follow1):
    async def GetRequest(Form):
        x= (await request.form).get(Form)
        #x = Form
        return x
    print("Creating" + ARun(GetRequest("Name")))
    #Name = ARun(GetRequest("Name"))
    if request.method == "POST":
        Name = DatabaseHandler.CheckName(ARun(GetRequest("Name")).lower().strip())
        User = DatabaseHandler.VerifyLogin(ARun(GetRequest("username")).lower().strip())
        Pass = DatabaseHandler.VerifyLogin(ARun(GetRequest("password")).strip())
        Pass2 = ARun(GetRequest("password2")).strip()
        return CreateAccount(Name,User,Pass,Pass2,Follow1)
        #return app.redirect(f"/createaccount/{Follow1}", 400)

@app.route("/CreateAccountCheck/<Follow1>/<Follow2>", methods = ["POST"])
def CreateAccountCheckTwoFollow(Follow1,Follow2):
    async def GetRequest(Form):
        x= (await request.form).get(Form)
        return x
    print("Creating" + ARun(GetRequest("Name")))
    if request.method == "POST":
        Name = DatabaseHandler.CheckName(ARun(GetRequest("Name")).lower().strip())
        User = DatabaseHandler.VerifyLogin(ARun(GetRequest("username")).lower().strip())
        Pass = DatabaseHandler.VerifyLogin(ARun(GetRequest("password")).strip())
        Pass2 = ARun(GetRequest("password2")).strip()
        return CreateAccount(Name,User,Pass,Pass2,f"{Follow1}/{Follow2}")

@app.route("/search", methods = ["GET"])
async def SearchPage():
    SearchInput = request.args.get('Search')
    Id = cache.get("id")
    if SearchInput is None or SearchInput == "":
        SearchDefault = ""
        return await quart.redirect("/home",302)
    else:
        SearchData = DatabaseHandler.SearchPosts(SearchInput)
        SearchDefault = str(SearchInput)
    #print(Data)
    return await render_template("Search.html",ID = Id,SearchInput = SearchDefault,Data = SearchData
                           )


def CreateAccount(Name,User,Pass,Pass2,Follow):
        if Name is None or User is None or Pass is None:
            ARun(FlashUser("Please Use Alphabetic Symbols or Symbols"))
        else:
            if Pass != Pass2:
                ARun(FlashUser("Both Passwords Must Be The Same"))
            else:
                AddAccount = DatabaseHandler.AddUserToDatabase([Name,User,Pass])
                if AddAccount == 201:
                    ARun(FlashUser("Sucsesfully Created Account"))
                    return app.redirect(f"/login/{Follow}",302)
                elif AddAccount == 409:
                    ARun(FlashUser("UserName Already Taken!"))


        return app.redirect(f"/createaccount/{Follow}",302)
    #return app.redirect(f"/createaccount/{Follow1}/{Follow2}", 400)



if __name__ == '__main__':
    #app.run(host = "0.0.0.0")
    app.run()