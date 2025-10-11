const delay = ms => new Promise(res => setTimeout(res, ms));
function SendLike(User,Value,PostID)
{
    //console.log(User,Value)
    let data = {
        "UserId": User,
        "PostId": PostID,
        "LikeValue": Value

    }
    fetch("http://"+location.host +"/likepost", {
        "method": "POST",
        "headers": {"Content-Type": "application/json"},
        "body": JSON.stringify(data),
    }).then(response => response.json())
        .then(data => console.log(data))
}
function updateLikes(ID)
{
    //console.log("Updating Like:"+ID)
    console.log("http://"+location.host +"/getLikes?ID="+ID)
    async function Request() {
        let obj;
        await delay(500);
        const res = await fetch("http://"+location.host +"/getLikes?ID="+ID)

        obj = await res.json();
        console.log(obj)
        //console.log('Like:'+ID + ":" +obj["Likes"])
        //console.log('Dislike:'+ID + ":" + obj["Dislikes"])
        document.getElementById('Like:'+ID).innerHTML = obj["Likes"] + '&nbsp👍';
        document.getElementById('Dislike:'+ID).innerHTML = obj["Dislikes"] + "&nbsp👎";

    }
    Request();
}