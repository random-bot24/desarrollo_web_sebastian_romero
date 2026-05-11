function nameValidation(name){
    if (!name) return false;
    let lengthValid = name.trim().length >= 3 && name.trim().length <=50
    let nameValid = /^[a-zA-Z\s]+$/.test(name);
    return lengthValid && nameValid;
}

function descriptionValidation(description){
    if (!description) return false;
    let lengthValid = description.trim().length >= 10 && description.trim().length <= 500;
    return lengthValid;
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
function validatePhone(phone){
    if (!phone) return false;
    let phoneRegex = /^\+?\d{9,14}$/;
    let phoneValid = phoneRegex.test(phone);
    return phoneValid;
}

function validateActivitiesForm(){
    let myFiles = document.getElementById("files").files;
    let myHours = document.getElementById("horas").value;
    let myDays = document.getElementById("days").value;
    let mySelect = document.getElementById("tipo-actividad").value;
    let myDescription = document.getElementById("description").value;
    let myName = document.getElementById("nombre").value;
    let validate = true;
    let invalidInputs = []
    function setinvalidInputs(input){
        invalidInputs.push(input);
        validate&&= false;
    }
    if (!nameValidation(myName)){
        setinvalidInputs("Nombre");
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
    if (!descriptionValidation(myDescription)){
        setinvalidInputs("Descripción");
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

function validateRegistrationMember(){
    let myName = document.getElementById("nombre").value;
    let myEmail = document.getElementById("email").value;
    let myPhone = document.getElementById("phone").value;
    let invalidInputs = [];
    let validate = true;
    let myRegion = document.getElementById("Region").value;
    let myComuna = document.getElementById("Comuna").value;
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
    if (!validatePhone(myPhone)){
        setinvalidInputs("Teléfono");
    }
    if (!myRegion){
        setinvalidInputs("Región");
    }
    if (!myComuna){
        setinvalidInputs("Comuna");
    }
    let validationBox = document.getElementById("val-boxMembers");
    let validationMsg = document.getElementById("val-msgMembers");
    let validationList = document.getElementById("val-listMembers");
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
        document.forms["Registro_miembros"].submit()
    }
}
let submitButtonMembers = document.getElementById("submit-btnMembers");
submitButtonMembers.addEventListener("click", (event) => {
    event.preventDefault();
    validateRegistrationMember();
});