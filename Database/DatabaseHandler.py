import sqlite3
from Database import SqlCommands

def GetLastUserID():
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        Result = Cursor.execute("SELECT AccountID FROM Account ORDER BY AccountID desc LIMIT 1").fetchone()
        return Result

def AddUserToDatabase(Values: list):
    #In the Format of ID NAME USERNAME(LOWERCASE) PASSWORD
    #It adds a new User To The Database
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()
        try:
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
        Result = Cursor.execute(SqlCommands.GetAllAccounts)
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
    with sqlite3.connect("Database/GymsyDatabase.db") as Connection:
        Cursor = Connection.cursor()

        
        Sucsessful = False
        Details = []
        Id = CheckUserNameAndPassword(Username,Password)
        if Id != 0:
            Sucsessful = True
            Details = GetUserByID(Id)
        return Sucsessful, Details
    return 0


print(AddUserToDatabase(["3","John","ieatkids","Testing23"]))
print(DeleteAccount(3))
print(GetAllAcounts())