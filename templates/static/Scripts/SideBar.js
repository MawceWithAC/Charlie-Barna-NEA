let IsBarOpen = true;

const CloseSideBar = {
    transform: ["scaleX(1)","scaleX(0)"]
};
const Forwards = {
    duration: 300,
    iterations: 1,
    direction: "normal"
};
const Backwards =  {...Forwards};
Backwards.direction = "reverse";


function SwapBar()
{
    const SideBar = document.querySelector(".sidebar");
	const Main = document.getElementById("Main");
    if (IsBarOpen) {
        SideBar.animate(CloseSideBar, Forwards);
        //SideBar.style.setProperty('--Display', 'None');
        setTimeout(() => {
            if (!IsBarOpen) {
                SideBar.style.setProperty('--Display', 'None');
				Main.style.width = "100%"
            }
        }, Forwards.duration-50);
        IsBarOpen = false;
    }
    else if (!IsBarOpen) {
        SideBar.style.setProperty('--Display', 'block')
		Main.style.width = "93%"
        SideBar.animate(CloseSideBar, Backwards);
        //SideBar.style.setProperty('--Display', 'None');
        IsBarOpen = true;
    }
    //console.log("Test")
}
function SwapBarInstant()
{
    const SideBar = document.querySelector(".sidebar");
	const Main = document.getElementById("Main");
    if (IsBarOpen) {
        SideBar.style.setProperty('--Display', 'None');
		Main.style.width = "100%"
        IsBarOpen = false;
    }
    else if (!IsBarOpen) {
        SideBar.style.setProperty('--Display', 'block')
		Main.style.width = "93%"
        IsBarOpen = true;
    }
    //console.log("Test")
}
if (screen.width < 500 || screen.width/screen.height >= 2
) 

{SwapBarInstant(); console.log(screen.width/screen.height)}