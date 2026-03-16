import sqlite3
from Database import SqlCommands, TimeFormatter
"""
Database Gets Accessed In This File Takes Sql From SqlCommands.py Takes Time Fromatting From TimeFormatter
"""
def VerifyLogin(Input: str):
    """
    Stops SQL Injection
    :param Input:
    :return:
    """
    for i in ["--"," "]:
        if i in Input:
            return None
    return Input

def CheckName(Input:str):
    """
    Stops SQl Injection
    :param Input:
    :return:
    """
    if "--" in Input:
        return None
    else:
        return Input

def GetPost(ID: int):
    """
    Retruns A Post With A Post ID
    :param ID:
    :return: Post Data (List)
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetPostsFromPostID.ReturnQuery([ID])).fetchone()
        return Result

def GetPostsFromExcersise(ID: int):
    """
    Gets Every Post From An Excersise
    :param ID:
    :return: 2D Array Of Posts
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetPostsFromExcersiseID.ReturnQuery([ID,ID])).fetchall()
        return Result

def GetPostsFromUser(Username: str):
    """
    Gets all the post from a user
    :param Username:
    :return: 2D Array Of Posts
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetPostsFromUserName.ReturnQuery([Username,Username])).fetchall()
        return Result


def GetUsernameFromID(ID: int ):
    """
    Gets A Username Given An ID
    :param ID:
    :return: Int ID
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        try:
            Result = Cursor.execute(SqlCommands.GetUsernameFromID.ReturnQuery(ID)).fetchone()
        except:
            return None
        if Result is not None:
            return Result[0]
        return Result

def GetIdFromUsername(User:str):
    """
    Get A Username Fron AN ID
    :param User:
    :return: String Name
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetIDFromUserName.ReturnQuery(User)).fetchone()
        if Result is not None:
            return Result[0]
        return Result

def GetLastUserID():
    """
    Gets The ID That The Last User Used
    :return: Int ID
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute("SELECT Max(AccountID) FROM Account").fetchone()
        return Result

def AddUserToDatabase(Values: list):
    """
    In the Format of NAME USERNAME(LOWERCASE) PASSWORD
    It adds a new User To The Database
    :param Values:
    :return: HTML Code (Int)
    """
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

def DeleteAccount(UserID: int):
    """
    Removes an Account From The Database

    !!!Unused!!!

    :param UserID:
    :return: True Or False Depending On If There Is An Error
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        try:
            Cursor.execute(SqlCommands.DeleteAccountFromID.ReturnQuery(UserID))
            return 1
        except Exception as e:
            print(e)
            return 0

def GetAllAcounts():
    """
    Returns All Accounts In The Database
    Debugging, Unused
    :return: 2D List Of All Accounts
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetAllAccounts)
        return Result.fetchall()

def GetComments(ParentID: int):
    """
    Gets All The Comments From A Ppst
    :param ParentID:
    :return: 2D Array Of Posts
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetPostComments.ReturnQuery([ParentID,ParentID]))
        return Result.fetchall()

    
def CheckUserNameAndPassword(Username:str, Password:str):
    """
    Takes in a Username and Password for a user
    and returns the ID that uses both of them
    :param Username:
    :param Password:
    :return: Int ID
    """

    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckResult = Cursor.execute(SqlCommands.FindAccountByLogin.ReturnQuery([Username,Password])).fetchall()
        if CheckResult != []:
            return CheckResult[0][0]
        return 0


def GetUserByID(ID:int):
    """
    Gets User Data From An ID
    :param ID:
    :return: Int ID or None if error
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.FindAccountByID.ReturnQuery([ID])).fetchone()
        if Result != ():
            return Result
        else:
            return None


def CheckLogin(Username:str, Password: str):
    """
    Returns Sucsesssful = True if Logged in,
    if you cant log in then return Sucsessful = False,
    Details Contails all the spare details of the program
    Format Of Details = (1, "Admin's Name", 'admin', 'Password', 1)
    :param Username:
    :param Password:
    :return: True If Sucsessful, And the details of the User in a List
    """

    Sucsessful = False
    Details = []
    Id = CheckUserNameAndPassword(Username,Password)
    if Id != 0:
        Sucsessful = True
        Details = GetUserByID(Id)
    return Sucsessful, Details

def GetExcersiseData(ExcersiseID: int):
    """
    Gets The Data Of The Excersise
    :param ExcersiseID:
    :return: List Of Data from excersise
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Results = Cursor.execute(SqlCommands.GetExcersiseData.ReturnQuery(ExcersiseID)).fetchone()
        return Results

def CreatePost(Values: list):
    """
    Format [Content:str, ExcersiseID:int,AccountID:int,Title:str]
    :param Values:
    :return: Post ID Int
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        #print("Connected")
        Cursor = Connection.cursor()
        LastPost = Cursor.execute(SqlCommands.GetLastPostId.ReturnQuery()).fetchone()
        Data = list(Values)
        Data.insert(0,int(LastPost[0])+1) #PostID
        Data.insert(5,str(TimeFormatter.GetDate()))
        Data.insert(6, str(TimeFormatter.GetTime()))
        #print(Data)
        try:
            Cursor.execute(SqlCommands.CreatePost.ReturnQuery(Data))
            return int(LastPost[0])+1
        except Exception as e:
            print(e)
            return None

def CreateComment(Values: list):
    """
    Creates A Comment, Simmilar to a post
    :param Values:
    :return: Html Status Code (INT)
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        inputValue = [int(Cursor.execute(SqlCommands.GetLastPostId.ReturnQuery()).fetchone()[0])+1, #PostID
        Values[0].strip(),#PostContent
        Values[1],#AccountID

        TimeFormatter.GetDate(),
        TimeFormatter.GetTime(),
        Values[2]] #Parent
        try:
            Cursor.execute(SqlCommands.CreateComment.ReturnQuery(inputValue))
            return 201
        except Exception as e:
            print(e)
            return 409

def AddLike(AccountID,PostID,Value):
    """
    Adds A like to a Post Or Comment
    :param AccountID:
    :param PostID:
    :param Value:
    :return: None
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckLike = Cursor.execute(SqlCommands.CheckLike.ReturnQuery([AccountID,PostID])).fetchone()
        if CheckLike is None:
            LastLike = Cursor.execute(SqlCommands.GetLastLikeId.ReturnQuery()).fetchone()[0]
            Cursor.execute(SqlCommands.AddLike.ReturnQuery([LastLike+1,PostID,AccountID,Value]))
        elif Value != CheckLike[1]:
            Cursor.execute(SqlCommands.UpdateLike.ReturnQuery([Value,CheckLike[0]]))
        else:
            Cursor.execute(SqlCommands.DeleteLike.ReturnQuery([CheckLike[0]]))


def GetMostPopularPosts(Amount: int):
    """
    Gets The {Amount} Most Popular Posts
    :param Amount:
    :return: 2D Array Of Post Data
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Results = Cursor.execute(SqlCommands.GetHomeExcersises.ReturnQuery(Amount)).fetchall()
        return Results

def GetLikes(PostID: int):
    """
    Returns The Likes And Dislikes Of A Post
    :param PostID:
    :return: Likes,Dislikes (INT)
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckLike = Cursor.execute(SqlCommands.GetLikes.ReturnQuery([PostID])).fetchone()
        if CheckLike is None:
            return 0,0
        return CheckLike[1],CheckLike[2]

def SearchPosts(SearchValue = "",ExcersiseID: int = -1):
    """
    Searches The Post, If Excersise Is Specified Only Get Posts From There
    :param SearchValue:
    :param ExcersiseID:
    :return: 2D Array Of Posts
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        SearchResults = Cursor.execute(SqlCommands.Search.ReturnQuery(SearchValue,ExcersiseID)).fetchall()
        return SearchResults


def GetAllExcersises():
    """
    Makes A 2D Array Of Excersise Details
    :return: 2D Array Of Excersise Details
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Results = Cursor.execute(SqlCommands.GetAllExcersises.ReturnQuery()).fetchall()
        return Results

def CreateExcerise(MuscleGroup,Name):
    """
    Creates A New Excersise
    :param MuscleGroup:
    :param Name:
    :return: ID Of New Exercise Or Existing Excersise
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        try:
            NextEx = Cursor.execute(SqlCommands.GetNextExcersiseId.ReturnQuery()).fetchone()[0]
            if Cursor.execute(SqlCommands.CheckDupeEx.ReturnQuery(Name)).fetchone() is None:
                Cursor.execute(SqlCommands.CreateExcersise.ReturnQuery([NextEx,MuscleGroup,Name]))
                return NextEx
            else:
                return Cursor.execute(SqlCommands.GetExceriseFromName.ReturnQuery(Name)).fetchone()[0]
        except Exception as e:
            print(e)

    return None

def SearchExcersises(SearchValue):
    """
    Searches All Excersise For A Specific One
    :param SearchValue:
    :return: 2D List Of Excersise Data
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        SearchResults = Cursor.execute(SqlCommands.SearchExcersises.ReturnQuery(SearchValue)).fetchall()
        #print(SearchResults)
        return SearchResults

def CreateList(Request:dict = {}):
    """
    Creates An Excersise List
    :param Request:
    :return: None
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        if Request["ID"] != "" and Request["Items"] != {}:
            #Create List
            LastList = Cursor.execute(SqlCommands.GetLastExcersiseListID.ReturnQuery()).fetchone()[0]
            if LastList is None:
                LastList = 1
            Cursor.execute(SqlCommands.MakeExcersiseList.ReturnQuery([LastList,Request["ID"],Request["Name"]]))
            for Index, Value in Request["Items"].items():
                #Create Items
                LastItem = Cursor.execute(SqlCommands.GetLastListItemID.ReturnQuery()).fetchone()[0]
                if LastItem is None:
                    LastItem = 1
                Cursor.execute(SqlCommands.AddExcersiseToList.ReturnQuery([LastItem,Value,LastList,Index]))

def GetExcersiseLists(UserID:int):
    """
    Gets Every Excersise List
    :param UserID:
    :return: Data Of Execrsise List as Json
    """
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        AllLists = Cursor.execute(SqlCommands.GetExcersiseListsFromID.ReturnQuery([UserID])).fetchall()
        if AllLists != []:
            Data = []
            for iLists in AllLists:
                #print(iLists[0])
                ListData = {"Name":iLists[1],"Excersises": []}
                for i in Cursor.execute(SqlCommands.GetExcersiseListItems.ReturnQuery([iLists[0]])).fetchall():
                    ListData["Excersises"].append(i)
                Data.append(ListData)
            return Data
        return None