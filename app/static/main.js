document.getElementById("expand").onclick = expand;
document.getElementById("close").onclick = close;

let navbarWidth = "175px";

function expand() {
    document.getElementById("main").style.marginLeft=navbarWidth;
}

function close() {
    document.getElementById("main").style.marginLeft="0%";
}