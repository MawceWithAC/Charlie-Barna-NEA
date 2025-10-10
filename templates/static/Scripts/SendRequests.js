function SendLike(User,Value,PostID)
{
    console.log(User,Value)
    let data = {
        "UserId": User,
        "LikeValue": Value,
        "PostId": PostID
    }
    fetch("/likepost", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    }).then(response => response.json())
        .then(data => console.log(data))
}