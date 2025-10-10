GetAllAccounts = "SELECT * FROM Account"

class Query():
    def __init__(self, content: str, additions: list = []):
        self.Query = content
        self.Additions = additions
    def ReturnQuery(self,NewContent: list = []):
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

#Get Posts Based On likes:
GetHomeExcersises = Query("""
SELECT p.PostID,
        p.Title,
        p.PostContent,
        p.ExcersiseID,
        COUNT(CASE l.LikeValue WHEN "1" then 1 end) AS Likes,
        COUNT(CASE l.LikeValue WHEN "-1" then -1 end) AS DisLikes,
        e.ExcersiseName,
        a.Username,
        p.Time,
        p.Date,
        sum(l.LikeValue) as LikeSum
FROM Post p, Likes l,Excersise e,Account a
WHERE p.PostID = l.PostID AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID AND p.Parent = 0
GROUP BY p.PostID
UNION
SELECT  p.PostID,
        p.Title,
        p.PostContent,
        p.ExcersiseID,
        0 AS Likes,
        0 AS Dislikes,
        e.ExcersiseName,
        a.Username,
        p.Time,
        p.Date,
        0 as LikeSum
FROM Post p, Excersise e, Account a
LEFT JOIN Likes l ON p.PostID = l.PostID
WHERE l.LikeValue IS NULL AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID AND p.Parent = 0
ORDER BY LikeSum desc,p.date desc ,p.time desc
limit {}
""", ["Amount"])
GetUsernameFromID = Query("""Select Username FROM Account WHERE AccountID = {}""",["ID"])
GetLastPostId = Query("SELECT Max(PostID) FROM Post")

CreatePost = Query("""
INSERT INTO Post
VALUES({},'{}',{},{},{},{},'{}','{}','{}')
""",["PostID",
    "PostContent",
     "ExcersiseID",
     "AccountID",
     "Likes",
     "Dislikes",
     "Title",
     "Date",
     "Time"
    ])
DeleteAccountFromID = Query("""DELETE FROM Account
WHERE AccountID = {};
""", ["ID"])
GetPostsFromExcersiseID = Query("""
SELECT p.PostID,
        p.Title,
        p.PostContent,
        p.ExcersiseID,
        COUNT(CASE l.LikeValue WHEN "1" then 1 end) AS Likes,
        COUNT(CASE l.LikeValue WHEN "-1" then -1 end) AS DisLikes,
        e.ExcersiseName,
        a.Username,
        p.Time,
        p.Date,
        sum(l.LikeValue) as LikeSum
FROM Post p, Likes l,Excersise e,Account a
WHERE p.PostID = l.PostID AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID And e.ExcersiseID = {} AND p.Parent = 0
GROUP BY p.PostID
UNION
SELECT  p.PostID,
        p.Title,
        p.PostContent,
        p.ExcersiseID,
        0 AS Likes,
        0 AS Dislikes,
        e.ExcersiseName,
        a.Username,
        p.Time,
        p.Date,
        0 as LikeSum
FROM Post p, Excersise e, Account a
LEFT JOIN Likes l ON p.PostID = l.PostID
WHERE l.LikeValue IS NULL AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID AND e.ExcersiseID = {} AND p.Parent = 0
ORDER BY LikeSum desc,p.date desc ,p.time desc
""",["ID","ID"])