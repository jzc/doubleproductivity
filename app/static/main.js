// document.getElementById("expand").onclick = expand;
// document.getElementById("close").onclick = close;

let navbarWidth = "175px";

// function expand() {
//     document.getElementById("main").style.marginLeft=navbarWidth;
//     document.getElementById("main").style.width = "calc(100% - 175px)";
// }

// function close() {
//     document.getElementById("main").style.marginLeft="0%";
//     document.getElementById("main").style.width="100%";
// }

flash_list = document.getElementById("flashes").children[0].children;
for (let i = 0; i < flash_list.length; i++)
{
    flash_list[i].children[0].onclick = function() {
        this.parentElement.remove()
    }
}

document.getElementsByClassName("hamburger")[0].onclick = function() {
    if (document.getElementById("main").style.width=="100%") 
    {
        document.getElementById("main").style.marginLeft=navbarWidth;
        document.getElementById("main").style.width = "calc(100% - 175px)";
    }
    else
    {
        document.getElementById("main").style.marginLeft="0%";
        document.getElementById("main").style.width="100%";
    }
}