function mostrarFoto(src) {
    const modal = document.createElement("div");
    modal.style.position = "fixed";
    modal.style.top = "0";
    modal.style.left = "0";
    modal.style.width = "100vw";
    modal.style.height = "100vh";
    modal.style.background = "rgba(0,0,0,0.8)";
    modal.style.display = "flex";
    modal.style.justifyContent = "center";
    modal.style.alignItems = "center";
    modal.innerHTML = `
        <div
            <img src = "${src}" width = "800" height ="600">
            <br>
            <button onclick = "this.parentElement.parentElement.remove()"> Cerrar </button>
        </div>
    `;
    document.body.appendChild(modal);
        
}


document.getElementById("add").addEventListener("click", function(){
    window.location.href = "add.html"
});

document.getElementById("view").addEventListener("click", function(){
    window.location.href = "view.html"
});

document.getElementById("stats").addEventListener("click", function(){
    window.location.href = "stats.html"
});