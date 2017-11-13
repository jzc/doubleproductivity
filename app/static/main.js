document.getElementById("expand").onclick = expand;
document.getElementById("close").onclick = close;

let navbarWidth = "175px";

function expand() {
    document.getElementById("main").style.marginLeft=navbarWidth;
    document.getElementById("main").style.width = "calc(100% - 175px)";
}

function close() {
    document.getElementById("main").style.marginLeft="0%";
    document.getElementById("main").style.width="100%";
}