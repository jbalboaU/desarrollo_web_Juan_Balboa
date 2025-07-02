const validateName = (name) => {
    if(!name) return false;
    let lengthValid = name.trim().length >= 0 && name.length <= 200;
    return lengthValid;
}

const validateEmail = (email) => {
    if (!email) return false;
    let lengthValid = email.length <= 100;
    let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    let formatValid = re.test(email);
    return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return true;
    let re = /^\+\d{7,15}$/;
    return re.test(phoneNumber);
};

const validateFiles = (files) => {
    if (!files || files.length === 0) return false;
    if (files.length > 5) return false;
    for (const file of files) {
        if (!file.type.startsWith("image/")) {
            return false;
        }
    }

    return true;
};


const validateSector = (sector) => {
    return sector.length <= 100;
};

const validateDateTime = (start, end) => {
    if (!start) return false;
    const startDate = new Date(start);
    if (end) {
        const endDate = new Date(end);
        return endDate > startDate;
    }
    return true;
};

const validateTema = (tema, otroTema) => {
    if (!tema) return false;
    if (tema === "otro") {
        return otroTema && otroTema.length >= 3 && otroTema.length <= 15;
    }
    return true;
};

const validateForm = () => {
    let myForm = document.forms["myForm"];
    let email = myForm["email"].value;
    let phoneNumber = myForm["celular"].value;
    let name = myForm["nombre"].value;
    let files = myForm["fotos"].files;
    let region = myForm["region"].value;
    let comuna = myForm["comuna"].value;
    let inicio = myForm["inicio"].value;
    let termino = myForm["termino"].value;
    let tema = myForm["tema"].value;
    let descripcionTema = myForm["descripcion_tema"].value;
    let sector = myForm["sector"].value;

    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid = false;
    };

    if (!validateName(name)) setInvalidInput("Nombre");
    if (!validateEmail(email)) setInvalidInput("Email");
    if (!validatePhoneNumber(phoneNumber)) setInvalidInput("Número de Celular");
    if (!validateFiles(files)) setInvalidInput("Fotos");
    if (!validateSelect(region)) setInvalidInput("Región");
    if (!validateSelect(comuna)) setInvalidInput("Comuna");
    if (!validateSelect(inicio)) setInvalidInput("Fecha de Inicio");
    if (!validateDateTime(inicio, termino)) setInvalidInput("Fecha de Término");
    if (!validateSelect(tema)) setInvalidInput("Tema");
    if (tema === "otro") {
        if (!descripcionTema || descripcionTema.length < 3 || descripcionTema.length > 15) {
            setInvalidInput("Descripción del tema (otros)");
        }
    }
    if (!validateSector(sector)) setInvalidInput("Sector");

    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");

    if (!isValid) {
        validationListElem.innerHTML = "";
        invalidInputs.forEach(input => {
            let li = document.createElement("li");
            li.textContent = input;
            validationListElem.appendChild(li);
        });
        validationMessageElem.textContent = "Los siguientes campos son inválidos:";
        validationBox.hidden = false;
        return false;
    } else {
        validationBox.hidden = true;
        return true;
    }
};

document.forms['myForm'].addEventListener('submit', (e) => {
    if (!validateForm()) {
        e.preventDefault();  // evita envío si hay errores
    }
});