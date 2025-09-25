let IsBarOpen = true;

const CloseSideBar = {
    transform: ["scaleX(1)","scaleX(0)"]
};
const test = [
    { transform: "rotate(0) scale(1)" },
    { transform: "rotate(360deg) scale(0)" },
];
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
        }, Forwards.duration-10);
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