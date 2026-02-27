//console.log("Loaded Redirect")
function RedirectTo(Location)
{/**/
//console.log(event.target.id +":" + this.id)
if (!ChildClickedBool){
window.location.href = Location; }
ChildClickedBool = false;
}
let ChildClickedBool = false;

function ChildClicked()
{
	ChildClickedBool = true;
	
}