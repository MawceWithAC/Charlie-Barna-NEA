GetAllAccounts = "SELECT * FROM Account"

class Query():
    def __init__(self, content: str, additions: list):
        self.Query = content
        self.Additions = additions
    def ReturnQuery(self,NewContent: list):
        #print(self.Query.format(*NewContent))
        if len(NewContent) == len(self.Additions):
            return self.Query.format(*NewContent)
        else:
            return "ERROR"
        
FindAccountByLogin = Query("SELECT * FROM Account WHERE Username = '{}' AND Password = '{}'", ["Username","Password"])
FindAccountByID = Query("SELECT * FROM Account WHERE AccountID = {}", ["ID"])
#AddUserToDatabase = Query("")