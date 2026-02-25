/*
Items = {"":"Please Choose", "1":"Bench Press", "2":"Squat",


}
*/

/*
{%for D in data%}
"{{d[0]}}":"{{d[1]}}",
{%endfor%}
*/

//var counter = 1;
function GenID()
{
    var randLetter = String.fromCharCode(65 + Math.floor(Math.random() * 26));
    var uniqid = randLetter + Date.now();
    return uniqid
}

function AppendToDiv(Items)
{

    let NewID = GenID();
    var DivToAppend = document.getElementById ("Appendable");

    NewElement = CreateTS(NewID,Items);
    DivToAppend.appendChild(NewElement);

    Tom = new TomSelect("#"+NewID, {
        create: false

    })
    Tom.setValue("")

}
function CreateTS(ID,Items)
{



    let TsSelector = document.createElement("select");
    TsSelector.required = true;
    TsSelector.classList.add("ts-inner");
    TsSelector.id = ID;

    //Create Options
    for (const [key, value] of Object.entries(Items)){
        let option = document.createElement("option");
        option.value = key;
        option.innerHTML = value;
        TsSelector.appendChild(option);
    }


    let DeleteButton = document.createElement("button");
    DeleteButton.addEventListener("click",deleteElement,false);
    DeleteButton.GetID = "Outer "+ID;
    DeleteButton.classList.add("deletebutton");
    DeleteButton.innerHTML = "X";


    let MoveDiv = ConstructMoveButtons(ID);




    let OutterDiv = document.createElement("div") ;
    OutterDiv.classList.add("newtom");
    OutterDiv.appendChild(TsSelector);
    OutterDiv.appendChild(DeleteButton);
    OutterDiv.appendChild(MoveDiv);


    FinalDiv = document.createElement("li")
    FinalDiv.appendChild(OutterDiv);
    FinalDiv.classList.add("listitem");
    FinalDiv.id = "Outer "+ID;
    return FinalDiv;
}
function ConstructMoveButtons(ID)
{
    let MoveDiv = document.createElement("div") ;
    MoveDiv.classList.add("movediv");

    UpButton = document.createElement("button");
    UpButton.GetDir = "U";
    UpButton.innerHTML = "&#8593;";
    UpButton.addEventListener("click",MoveElement,false);
    UpButton.GetID = "Outer "+ID;
    UpButton.type = "Button"

    DownButton = document.createElement("button");
    DownButton.GetDir = "D";
    DownButton.innerHTML = "&#8595;";
    DownButton.addEventListener("click",MoveElement,false);
    DownButton.GetID = "Outer "+ID;
    DownButton.type = "Button"

    MoveDiv.appendChild(UpButton);
    MoveDiv.appendChild(DownButton);

    return MoveDiv;
}

function deleteElement(evt)
{

    let element = document.getElementById(evt.currentTarget.GetID);
    element.remove();

}
function MoveElement(evt)
{
    let Direction = evt.currentTarget.GetDir;
    let ID = evt.currentTarget.GetID;
    let self = document.getElementById(ID)

    let container = document.getElementById("Appendable")

    let index = Array.prototype.indexOf.call(container.childNodes, self)
    console.log(index)
    if (Direction == "U")
    {container.insertBefore(self,self.previousElementSibling)
    }
    else
    {container.insertBefore(self.nextElementSibling,self);}
    //console.log(Direction + ID);
    //let AllElements = document.getElementsByClassName("newtom")

}