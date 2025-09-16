import sqlite3
from Database import SqlCommands




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

print(GetUserByID(CheckUserNameAndPassword("admin","Testing23")))
