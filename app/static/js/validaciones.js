function nameValidation(name){
    if (!name) return false;
    let lengthValid = name.trim().length >= 3 && name.trim().length <=50
    let nameValid = /^[a-zA-Z\s]+$/.test(name);
    return lengthValid && nameValid;
}

function emailValidation(email){
    if (!email) return false;
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    let emailValid = emailRegex.test(email);
    return emailValid;
}

function validateFiles(files){
    if (!files) return false;
    let lengthValid = 1 <= files.length && files.length <= 2;
    let typeValid = true;
    for (const file of files){
        let fileFamily = file.type.split("/")[0];
        typeValid = typeValid && (fileFamily === "image");
    }
    return lengthValid && typeValid;
}
function validateHoursPerWeek(hours){
    if (!hours) return false;
    let hoursValid = Number.isInteger(Number(hours)) && Number(hours) >= 1 && Number(hours) <= 40;
    return hoursValid;
}
function validateDaysPerWeek(days){
    if (!days) return false;
    let hoursValid = Number.isInteger(Number(days)) && Number(days) >= 1 && Number(days) <= 7;
    return hoursValid;
}
function validateSelect(select){
    if (!select) return false;
    return true;
}

function validateForm(){
    let myName = document.getElementById("nombre").value;
    let myEmail = document.getElementById("email").value;
    let myFiles = document.getElementById("files").files;
    let myHours = document.getElementById("horas").value;
    let myDays = document.getElementById("days").value;
    let mySelect = document.getElementById("tipo-actividad").value;
    let validate = true;
    let invalidInputs = []
    function setinvalidInputs(input){
        invalidInputs.push(input);
        validate&&= false;
    }
    if (!nameValidation(myName)){
        setinvalidInputs("Nombre");
    }
    if (!emailValidation(myEmail)){
        setinvalidInputs("Email");
    }
    if (!validateSelect(mySelect)){
        setinvalidInputs("Tipo de actividad");
    }
    if (!validateDaysPerWeek(myDays)){
        setinvalidInputs("Dias");
    }
    if (!validateHoursPerWeek(myHours)){
        setinvalidInputs("Horas");
    }
    if (!validateFiles(myFiles)){
        setinvalidInputs("Archivo");
    }


    let validationBox = document.getElementById("val-box");
    let validationMsg = document.getElementById("val-msg");
    let validationList = document.getElementById("val-list");
    if (!validate){
        validationList.textContent = "";
        // agregar elementos inválidos al elemento val-list.
        for (input of invalidInputs) {
            let listElement = document.createElement("li");
            listElement.innerText = input;
            validationList.append(listElement);
        }
        // establecer val-msg
        validationMsg.innerText = "Los siguientes campos son inválidos:";

        // aplicar estilos de error
        validationBox.style.backgroundColor = "#ffdddd";
        validationBox.style.borderLeftColor = "#f44336";

        // hacer visible el mensaje de validación
        validationBox.hidden = false;
        validationBox.scrollIntoView({behavior: "smooth"});
    }
    else{
        validationBox.hidden = true;
        alert("Formulario enviado correctamente");
        window.location.href = "main.html";
    }
}
let submitButton = document.getElementById("submit-btn");
submitButton.addEventListener("click", (event) => {
    event.preventDefault();
    validateForm();
});