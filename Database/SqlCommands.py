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
            print(NewContent, self.Additions)
            return "ERROR building Query"

class SearchQuery(Query):
    def __init__(self,content):
        super().__init__(content)

    def BuildQuery(self,SearchWords,Column):
        Adding = f"{Column} LIKE '%{SearchWords[0]}%'"
        for Value in SearchWords[1:]:
            Adding += f" \n AND {Column} LIKE '%{Value}%'"

        return self.Query + "WHERE " + Adding

    def ReturnQuery(self,SearchDetails: str = "",ExcersiseID: int = -1):
        SearchWords = SearchDetails.split()
        if SearchWords != []:
            if ExcersiseID == -1:
                return (self.BuildQuery(SearchWords,"ExcersiseName")
                        + "  UNION  " + self.BuildQuery(SearchWords,"Title")+ "  UNION  "
                        + self.BuildQuery(SearchWords,"PostContent"))
            else:
                return (f"SELECT * FROM (" +self.BuildQuery(SearchWords,"Title")+ "  UNION  "
                        + self.BuildQuery(SearchWords,"PostContent") +f") WHERE ExcersiseID = '{ExcersiseID}'" )
        else:
            return self.Query


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
#Get Comments Of A Post
GetPostComments = Query("""
SELECT p.PostID,
		a.Username,
        p.PostContent,
        COUNT(CASE l.LikeValue WHEN "1" then 1 end)/2 AS Likes,
        COUNT(CASE l.LikeValue WHEN "-1" then -1 end)/2 AS DisLikes,
        p.Date,
        p.Time,
        sum(l.LikeValue) as LikeSum,
		p.Parent
FROM Post p, Likes l,Excersise e,Account a
WHERE p.PostID = l.PostID  AND a.AccountID = p.AccountID AND p.Parent = {}
GROUP BY p.PostID
UNION
SELECT  p.PostID,
        a.Username,
        p.PostContent,
        0 AS Likes,
        0 AS Dislikes,
        p.Date,
        p.Time,
        0 as LikeSum,
		p.Parent
FROM Post p, Excersise e, Account a
LEFT JOIN Likes l ON p.PostID = l.PostID
WHERE l.LikeValue IS NULL AND a.AccountID = p.AccountID AND p.Parent = {}
ORDER BY LikeSum desc,p.date desc ,p.time desc

""",["ParentID","ParentID"])
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

#This Needs Updating
CreatePost = Query(""" 
INSERT INTO Post
VALUES({},'{}',{},{},{},{},'{}','{}','{}')
""",["PostID",
    "PostContent",
     "ExcersiseID",
     "AccountID",
     "Title",
     "Date",
     "Time"
    ])
CreateComment = Query(""" 
INSERT INTO Post
VALUES({},'{}',0,{},"Comment",'{}','{}',{})
""",["PostID",
    "PostContent",
     "AccountID",
     "Date",
     "Time",
     "Parent"
    ])



#########
DeleteAccountFromID = Query("""DELETE FROM Account
WHERE AccountID = {};
""", ["ID"])
GetPostsFromPostID = Query("""
SELECT * 
FROM (SELECT p.PostID,
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
WHERE l.LikeValue IS NULL AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID AND p.Parent = 0)
WHERE PostID = {}
""",["PostID"]  )

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

CheckLike = Query("SELECT LikeID,LikeValue FROM Likes WHERE AccountID = {} AND PostID = {}",["AccountID","PostID"])
AddLike = Query("INSERT INTO Likes VALUES({},{},{},{})",["LikeID","PostID","AccountID","LikeValue"])
GetLastLikeId = Query("SELECT Max(LikeID) FROM Likes")
UpdateLike = Query("UPDATE Likes SET LikeValue = {} WHERE LikeID = {}",["LikeValue","LikeID"])
GetLikes = Query("""SELECT PostID,  COUNT(CASE LikeValue WHEN "1" then 1 end) AS Likes,
        COUNT(CASE LikeValue WHEN "-1" then -1 end) AS DisLikes
    FROM Likes
    WHERE PostID = {}
group by PostID""",["PostID"])
DeleteLike = Query("DELETE FROM Likes WHERE LikeID = {}",["LikeID"])
Search = SearchQuery("""SELECT * FROM (
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
WHERE p.PostID = l.PostID AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID
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
WHERE l.LikeValue IS NULL AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID
ORDER BY LikeSum desc,p.date desc ,p.time desc)
""")