document.addEventListener("DOMContentLoaded", function() {
    let regionSelect = document.getElementById("region");
    let comunaSelect =document.getElementById("comuna");
    const allComunas = Array.from(comunaSelect.options).slice(1);

    function filtrarComunas() {
        let regionId=regionSelect.value;
        comunaSelect.innerHTML = '<option value="">Seleccione una comuna</option>';

        let comunasFiltradas = allComunas.filter(option => option.dataset.region === regionId);
        comunasFiltradas.forEach(option => comunaSelect.appendChild(option));
    }

    regionSelect.addEventListener("change", filtrarComunas);

    if (regionSelect.value) {
        filtrarComunas();
    }
});


function activateContactoId() {
    const contactarPor= document.getElementById("contactar_por");
    const contactoId = document.querySelector("label[for = 'contacto_id']");
    const textContactoId = document.getElementById("contacto_id");

    if(contactarPor.value !== ""){
        contactoId.style.display = "block";
        textContactoId.style.display = "block";
    } else {
        contactoId.style.display = "none";
        textContactoId.style.display = "none";
    }
}


function activateDescripcionTema() {
    const tema = document.getElementById("tema");
    const descripcionTema = document.querySelector("label[for = 'descripcion_tema']");
    const textDescripcionTema = document.getElementById("descripcion_tema");

    if(tema.value === "otro"){
        descripcionTema.style.display = "block";
        textDescripcionTema.style.display = "block";
    } else {
        descripcionTema.style.display = "none";
        textDescripcionTema.style.display = "none";
    }
}

document.getElementById("contactar_por").addEventListener("change", activateContactoId);
document.getElementById("tema").addEventListener("change", activateDescripcionTema);

window.onload = () => {
    activateContactoId();
    activateDescripcionTema();
    document.getElementById("val-box").hidden = true;
};