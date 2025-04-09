const validateName = (name) => {
    if(!name) return false;
    let lengthValid = name.trim().length >= 4;
    
    return lengthValid;
}

const validateEmail = (email) => {
    if (!email) return false;
    let lengthValid = email.length > 15;

    // validamos el formato
    let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    let formatValid = re.test(email);

    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return false;
    // validación de longitud
    let lengthValid = phoneNumber.length >= 8;
    // validación de formato
    let re = /^[0-9]+$/;
    let formatValid = re.test(phoneNumber);
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
};

const validateFiles = (files) => {
    if (!files) return false;

    // validación del número de archivos
    let lengthValid = 1 <= files.length && files.length <= 3;
    // validación del tipo de archivo
    let typeValid = true;
    for (const file of files) {
      // el tipo de archivo debe ser "image/<foo>" o "application/pdf"
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
    }

    // devolvemos la lógica AND de las validaciones.
    return lengthValid && typeValid;
};

const validateForm = ()=>{
    let myForm = document.forms["myForm"];
    let email = myForm["email"].value;
    let phoneNumber = myForm["phone"].value;
    let name = myForm["nombre"].value;
    let files = myForm["files"].files;
    let region = myForm["region-select"].value;
    let comuna = myForm["comuna-select"].value;
    let inicio = myForm["inicio"].value;
    let tema = myForm["tema-select"].value;


    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
    invalidInputs.push(inputName);
    isValid &&= false;
    };

    if (!validateName(name)) {
    setInvalidInput("Nombre");
    }
    if (!validateEmail(email)) {
    setInvalidInput("Email");
    }
    if (!validatePhoneNumber(phoneNumber)) {
    setInvalidInput("Número de Celular");
    }
    if (!validateFiles(files)) {
    setInvalidInput("Fotos");
    }
    if (!validateSelect(region)) {
    setInvalidInput("Region");
    }
    if (!validateSelect(comuna)) {
    setInvalidInput("Comuna");
    }
    if (!validateSelect(tema)) {
        setInvalidInput("Tema");
    }
    if (!validateSelect(inicio)) {
        setInvalidInput("Fecha de Inicio");
    }

    // finalmente mostrar la validación
    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");
    let formContainer = document.querySelector(".main-container");

    if (!isValid) {
        validationListElem.textContent = "";

        for (input of invalidInputs) {
            let listElement = document.createElement("li");
            listElement.innerText = input;
            validationListElem.append(listElement);
        }
        validationMessageElem.innerText = "Los siguientes campos son inválidos:";
        validationMessageElem.style.padding = "6px";
        validationMessageElem.style.textAlign = "center";
        
        
        validationBox.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
        validationBox.style.borderRadius = "3px";
        validationBox.style.fontFamily = "sans-serif";
        validationBox.style.color = "rgba(130, 255, 212)";
        validationBox.style.textAlign = "left";
        validationBox.style.paddingBottom = "3px";

        validationBox.hidden = false;
    } else {
      // Ocultar el formulario
        myForm.style.display = "none";

          // establecer mensaje de éxito
        validationMessageElem.innerText = "¿Está seguro que desea agregar esta actividad?";
        validationListElem.textContent = "";
        validationMessageElem.style.padding = "6px";
        validationMessageElem.style.textAlign = "center";
          
        validationBox.style.backgroundColor = "rgba(0, 0, 0, 0.7)";
        validationBox.style.borderRadius = "3px";
        validationBox.style.fontFamily = "sans-serif";
        validationBox.style.color = "rgba(130, 255, 212)";
        validationBox.style.textAlign = "left";
        validationBox.style.paddingBottom = "3px";

          // Agregar botones para enviar el formulario o volver
        let submitButton = document.createElement("button");
        submitButton.innerText = "Sí, estoy seguro";
        submitButton.style.margin = "20px";
        submitButton.style.padding ="8px";
        submitButton.style.borderRadius ="5px";
        submitButton.style.border ="None";
        submitButton.style.fontSize ="16px";
        submitButton.style.fontFamily ="sans-serif";
        submitButton.style.textTransform ="uppercase";
        submitButton.style.fontWeight ="bold";
        submitButton.style.backgroundColor ="rgba(130, 255, 212)";
        submitButton.style.color ="rgba(0, 0, 0, 0.7)";

        submitButton.addEventListener("click", () => {
        // myForm.submit();
        // no tenemos un backend al cual enviarle los datos
    });

    let backButton = document.createElement("button");
    backButton.innerText = "No, no estoy seguro, quiero volver al formulario";
    submitButton.innerText = "Sí, estoy seguro";
    backButton.style.margin = "20px";
    backButton.style.padding ="8px";
    backButton.style.borderRadius ="5px";
    backButton.style.border ="None";
    backButton.style.fontSize ="16px";
    backButton.style.fontFamily ="sans-serif";
    backButton.style.textTransform ="uppercase";
    backButton.style.fontWeight ="bold";
    backButton.style.backgroundColor ="rgba(130, 255, 212)";
    backButton.style.color ="rgba(0, 0, 0, 0.7)";
    
    
    backButton.addEventListener("click", () => {
        // Mostrar el formulario nuevamente
        myForm.style.display = "block";
        validationBox.hidden = true;
    });

    validationListElem.appendChild(submitButton);
    validationListElem.appendChild(backButton);

      // hacer visible el mensaje de validación
    validationBox.hidden = false;
    }
};

const validateSelect = (select) => {
    if(!select) return false;
    return true
}

let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);
