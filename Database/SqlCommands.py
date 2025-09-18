GetAllAccounts = "SELECT * FROM Account"

class Query():
    def __init__(self, content: str, additions: list):
        self.Query = content
        self.Additions = additions
    def ReturnQuery(self,NewContent: list):
        #print(self.Query.format(*NewContent))
        if type(NewContent) != list:
            NewContent = [NewContent]
        if len(NewContent) == len(self.Additions):
            return self.Query.format(*NewContent)
        else:
            return "ERROR"
        
FindAccountByLogin = Query("SELECT * FROM Account WHERE Username = '{}' AND Password = '{}'"
                           , ["Username","Password"])

FindAccountByID = Query("SELECT * FROM Account WHERE AccountID = {}"
                        , ["ID"])

AddUserToDatabase = Query("INSERT INTO Account VALUES({},'{}','{}','{}',0)"
                          ,["UserID","Name","Username","Password"])

GetExcersiseData = Query("""SELECT * FROM Excersise NATURAL JOIN MuscleGroup
--ON Excersise.MuscleID = MuscleGroup.MuscleID
WHERE ExcersiseID == {}""",
                         ["ExcersiseID"])

#Get Posts Based On Time:
GetListExcersises = Query("""
SELECT p.PostID, p.Title, p.PostContent, p.ExcersiseID, p.Likes, p.Dislikes,e.ExcersiseName,a.Username,p.time,p.date
FROM Post p NATURAL JOIN Excersise e
INNER JOIN Account a
ON p.AccountID == a.AccountID
ORDER BY p.Likes
LIMIT {}
""", ["Amount"])
#ORDER BY p.date , p.time