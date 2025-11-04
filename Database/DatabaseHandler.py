import sqlite3
from Database import SqlCommands, TimeFormatter
def VerifyLogin(Input: str):
    for i in ["--"," "]:
        if i in Input:
            return None
    return Input
def CheckName(Input:str):
    if "--" in Input:
        return None
    else:
        return Input
def GetPost(ID: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetPostsFromPostID.ReturnQuery([ID])).fetchone()
        return Result

def GetPostsFromExcersise(ID: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        #print(SqlCommands.GetPostsFromExcersiseID.ReturnQuery([ID,ID]))
        Result = Cursor.execute(SqlCommands.GetPostsFromExcersiseID.ReturnQuery([ID,ID])).fetchall()
        return Result
    

    pass
def GetUsernameFromID(ID: int ):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetUsernameFromID.ReturnQuery(ID)).fetchone()
        if Result is not None:
            return Result[0]
        return Result
    
def GetLastUserID():
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute("SELECT Max(AccountID) FROM Account").fetchone()
        return Result
def AddUserToDatabase(Values: list):
    #In the Format of NAME USERNAME(LOWERCASE) PASSWORD
    #It adds a new User To The Database
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Values.insert(0,int(GetLastUserID()[0])+1)
        try:
            print(SqlCommands.AddUserToDatabase.ReturnQuery(Values))
            Cursor.execute(SqlCommands.AddUserToDatabase.ReturnQuery(Values))
            return 201
        except Exception as e:
            print(e)
            return 409
    return 0

def DeleteAccount(UserID: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        try:
            Cursor.execute(SqlCommands.DeleteAccountFromID.ReturnQuery(UserID))
            return 1
        except Exception as e:
            print(e)
            return 0
def UpdateUserDetails(Colomn:str, Value:any):
    pass

def GetAllAcounts(): #Returns every single account in the database as a 2D list
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetAllAccounts.ReturnQuery())
        return Result.fetchall()
    return 0

    
def CheckUserNameAndPassword(Username:str, Password:str):
    #Takes in a Username and Password for a user
    #and returns the ID that uses both of them
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckResult = Cursor.execute(SqlCommands.FindAccountByLogin.ReturnQuery([Username,Password])).fetchall()
        if CheckResult != []:
            return CheckResult[0][0]
        return 0
    return 0

def GetUserByID(ID:int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.FindAccountByID.ReturnQuery([ID])).fetchone()
        if Result != ():
            return Result
        else:
            return None
    return 404

def CheckLogin(Username:str, Password: str):
        
    #Returns Sucsesssful = True if Logged in,
    #if you cant log in then return Sucsessful = False,
    #Details Contails all the spare details of the program
    #Format Of Details = (1, "Admin's Name", 'admin', 'Testing23', 1)
    Sucsessful = False
    Details = []
    Id = CheckUserNameAndPassword(Username,Password)
    if Id != 0:
        Sucsessful = True
        Details = GetUserByID(Id)
    return Sucsessful, Details
    

def GetExcersiseData(ExcersiseID: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Results = Cursor.execute(SqlCommands.GetExcersiseData.ReturnQuery(ExcersiseID)).fetchone()
        return Results
    return 0

def CreatePost(Values: list): # [Content:str, ExcersiseID:int,AccountID:int,Title:str]
    # Needs To Be Updated To New Post Format
    #
    ##
   with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        LastPost = Cursor.execute(SqlCommands.GetLastPostId.ReturnQuery()).fetchone()
        Values.insert(0,int(LastPost[0])+1) 
        Values.insert(4,0)
        Values.insert(5,0)
        Values.insert(7,TimeFormatter.GetDate())
        Values.insert(8,TimeFormatter.GetTime())
        try:
            print(SqlCommands.CreatePost.ReturnQuery(Values))
            Cursor.execute(SqlCommands.CreatePost.ReturnQuery(Values))
            return 201
        except Exception as e:
            print(e)
            return 409

def AddLike(AccountID,PostID,Value):
    print(AccountID,PostID,Value)
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckLike = Cursor.execute(SqlCommands.CheckLike.ReturnQuery([AccountID,PostID])).fetchone()
        print(CheckLike)
        if CheckLike is None:
            LastLike = Cursor.execute(SqlCommands.GetLastLikeId.ReturnQuery()).fetchone()[0]
            Cursor.execute(SqlCommands.AddLike.ReturnQuery([LastLike+1,PostID,AccountID,Value]))
        elif Value != CheckLike[1]:
            print(SqlCommands.UpdateLike.ReturnQuery([Value,CheckLike[0]]))
            Cursor.execute(SqlCommands.UpdateLike.ReturnQuery([Value,CheckLike[0]]))
        else:
            Cursor.execute(SqlCommands.DeleteLike.ReturnQuery([CheckLike[0]]))


def GetMostPopularPosts(Amount: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Results = Cursor.execute(SqlCommands.GetHomeExcersises.ReturnQuery(Amount)).fetchall()
        return Results

def GetLikes(PostID: int):
    print(PostID)
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckLike = Cursor.execute(SqlCommands.GetLikes.ReturnQuery([PostID])).fetchone()
        if CheckLike is None:
            return 0,0
        return CheckLike[1],CheckLike[2]

def SearchPosts(SearchValue = "",ExcersiseID: int = -1):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        print(SqlCommands.Search.ReturnQuery(SearchValue,ExcersiseID))
        SearchResults = Cursor.execute(SqlCommands.Search.ReturnQuery(SearchValue,ExcersiseID)).fetchall()
        #print(SearchResults)
        return SearchResults
#CreatePost(["This Is A Test2",1,2,"JustTestingThePostFunction"])
#print(GetExcersiseData([1]))
#print(AddUserToDatabase(["iwonder","whereillbe","Testing23"]))
#print(DeleteAccount(4))
#print(GetAllAcounts())
#print()
#AddLike(10,10,-1)