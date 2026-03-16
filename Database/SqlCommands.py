GetAllAccounts = "SELECT * FROM Account"
"""
This Contains All The SQL
"""


class Query:
    """
    Query Builder Returns A Formateed SQL Command
    """
    def __init__(self, content: str, additions: list = []):
        self.Query = content
        self.Additions = additions

    def ReturnQuery(self,NewContent: list = []):
        """
        Builds A Query And Returns It With Inputted Details
        :param NewContent:
        :return:
        """
        if type(NewContent) != list:
            NewContent = [NewContent]
        if len(NewContent) == len(self.Additions):
            return self.Query.format(*NewContent)
        else:
            print(NewContent, self.Additions)
            return "ERROR building Query"

class SearchQuery(Query):
    """
    Child Of Query, Builds A Search For The Search Bars
    """
    def __init__(self,content):
        super().__init__(content)

    def BuildQuery(self,SearchWords,Column):
        """
        Creates A Query
        :param SearchWords:
        :param Column:
        :return: String containing part of the SQL
        """
        Adding = f"{Column} LIKE '%{SearchWords[0]}%'"
        for Value in SearchWords[1:]: #Skips the first word
            Adding += f" \n AND {Column} LIKE '%{Value}%'"
        return self.Query + "WHERE " + Adding

    def ReturnQuery(self,SearchDetails: str = "",ExcersiseID: int = -1):
        SearchWords = SearchDetails.split()
        if SearchWords != []:
            if ExcersiseID == -1: #If No Excersise Has Been Selected
                return (self.BuildQuery(SearchWords,"ExcersiseName")
                        + "  UNION  " + self.BuildQuery(SearchWords,"Title")+ "  UNION  "
                        + self.BuildQuery(SearchWords,"PostContent"))
            else: #If An Excersise has Been Selected
                return (f"SELECT * FROM (" +self.BuildQuery(SearchWords,"Title")+ "  UNION  "
                        + self.BuildQuery(SearchWords,"PostContent") +f") WHERE ExcersiseID = '{ExcersiseID}'" )
        else: #Redturns a search of all
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

GetIDFromUserName = Query("""Select AccountID FROM Account WHERE Username = '{}'""",["Username"])

GetLastPostId = Query("SELECT Max(PostID) FROM Post")


CreatePost = Query(""" 
INSERT INTO Post
VALUES({},'{}',{},{},'{}','{}','{}',0)
""",["PostID",
    "PostContent",
     "ExcersiseID",
     "AccountID",
     "Date",
    "Title",
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

GetPostsFromUserName = Query("""
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
WHERE p.PostID = l.PostID AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID And a.Username = '{}' AND p.Parent = 0
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
WHERE l.LikeValue IS NULL AND e.ExcersiseID = p.ExcersiseID AND a.AccountID = p.AccountID AND a.Username = '{}' AND p.Parent = 0
ORDER BY LikeSum desc,p.date desc ,p.time desc
""",["Username","Username"])


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
GetAllExcersises = Query("SELECT e.ExcersiseID,e.ExcersiseName FROM Excersise e")
CreateExcersise = Query(""" 
INSERT INTO Excersise
VALUES({},{},'{}')
""",["ExcersiseID",
     "MuscleID",
     "ExcersiseName"
    ])
GetNextExcersiseId = Query("SELECT Max(ExcersiseID)+1 FROM Excersise")
SearchExcersises = Query("""SELECT * FROM Excersise
WHERE ExcersiseName LIKE "%{}%"
"""
                         ,["SearchData"])
CheckDupeEx = Query("""SELECT * FROM Excersise
WHERE ExcersiseName = '{}' """,["Name"])

GetExceriseFromName = Query("""SELECT ExcersiseID FROM Excersise
WHERE ExcersiseName = '{}' """,["name"])

GetLastExcersiseListID = Query("SELECT Max(ExcersiseListId)+1 FROM ExcersiseList")
MakeExcersiseList = Query("""INSERT INTO ExcersiseList VALUES({},{},"{}")""",
                           ["ListID","AccountID","Name"])
AddExcersiseToList = Query("""INSERT INTO ListItems VALUES({},{},{},{})""",["ItemID","ExcersiseID","ExcersiseListID","Index"])
GetLastListItemID = Query("SELECT Max(ItemID)+1 FROM ListItems")
GetExcersiseListsFromID = Query("SELECT ExcersiseListID,Name FROM ExcersiseList WHERE AccountID = {}",["AccountID"])
GetExcersiseListItems = Query("""
SELECT l.ExcersiseID,e.ExcersiseName
FROM ListItems l, Excersise e
WHERE l.ExcersiseID = e.ExcersiseID AND l.ExcersiseListID = 1
ORDER BY Location
""",["ListID"])