import sqlite3
from Database import SqlCommands
def StopSQlnjection(Input: str):
    if "--" not in Input:
        return Input
    else:
        return None
def GetPostsFromExcersise(ID: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetPostsFromExcersiseID.ReturnQuery(ID)).fetchall()
        return Result
    
    
def GetUsernameFromID(ID: int ):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetUsernameFromID.ReturnQuery(ID)).fetchone()
        return Result
    
def GetLastUserID():
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute("SELECT AccountID FROM Account ORDER BY AccountID desc LIMIT 1").fetchone()
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
            Cursor.execute(f"DELETE FROM Account WHERE AccountID = {UserID}")
            return 1
        except Exception as e:
            print(e)
            return 0
def UpdateUserDetails(Colomn:str, Value:any):
    pass

def GetAllAcounts(): #Returns every single account in the database as a 2D list
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute(SqlCommands.GetAllAccounts.returnQuery())
        return Result.fetchall()
    return 0

    
def CheckUserNameAndPassword(Username:str, Password:str):
    #Takes in a Username and Password for a user
    #and returns the ID that uses both of them
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        CheckResult = Cursor.execute(SqlCommands.FindAccountByLogin.ReturnQuery([Username.lower(),Password])).fetchall()
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

def GetMostPopularPosts(Amount: int):
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Results = Cursor.execute(SqlCommands.GetListExcersises.ReturnQuery(Amount)).fetchall()
        return Results
    return 0
#print(GetExcersiseData([1]))
#print(AddUserToDatabase(["John","ieatkids","Testing23"]))
#print(DeleteAccount(3))
#print(GetAllAcounts())
#print()