// Función para destacar el texto que calza con el patrón buscado 
function resaltarTexto(texto, patron) {
    if (!patron || !texto) return texto;
    // Creamos una expresión regular 
    const regex = new RegExp(`(${patron})`, 'gi');
    return texto.toString().replace(regex, '<mark>$1</mark>');
}


function enviarEvaluacion(idActividad) {
    // Capturamos el valor ingresado
    const inputNota = document.getElementById(`input-nota-${idActividad}`);
    const valorNota = parseInt(inputNota.value, 10);

    if (isNaN(valorNota) || valorNota < 1 || valorNota > 7) {
        alert("Por favor, ingresa un número entero entre 1 y 7.");
        return;
    }

    fetch(`/api/actividades/${idActividad}/evaluar?valorNota=${valorNota}`, {
        method: 'POST'
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error al guardar la evaluación");
        }
        return response.json(); // Esperamos el nuevo promedio recalculado
    })
    .then(nuevoPromedio => {
        const spanNota = document.getElementById(`nota-texto-${idActividad}`);
        
        spanNota.innerText = nuevoPromedio.toFixed(1); 
        
        inputNota.value = '';
        
        alert("¡Nota guardada con éxito!");
    })
    .catch(error => {
        console.error(error);
        alert("Hubo un problema al conectar con el servidor.");
    });
}


// Esperamos a que el HTML cargue completamente
document.addEventListener("DOMContentLoaded", function() {
    const inputBuscador = document.getElementById("input-buscador");
    const contenedorResultados = document.getElementById("contenedor-resultados");

    // Escuchamos cada vez que el usuario escribe en el input
    inputBuscador.addEventListener("input", function() {
        const textoBusqueda = inputBuscador.value.trim();

        // 1. Validar que haya escrito al menos 3 caracteres 
        if (textoBusqueda.length >= 3) {
            
            // 2. Llamada asíncrona al endpoint de búsqueda 
            fetch(`/api/actividades/buscar?q=${textoBusqueda}`)
                .then(response => {
                    if (!response.ok) throw new Error("Error en la red");
                    return response.json();
                })
                .then(datos => {
                    // Limpiamos resultados anteriores
                    contenedorResultados.innerHTML = "";

                    // 3. Si no hay resultados, mostramos el mensaje apropiado 
                    if (datos.length === 0) {
                        contenedorResultados.innerHTML = "<p>No se encontraron actividades con ese término.</p>";
                        return;
                    }

                    // 4. Iterar sobre los datos y construir el HTML 
                    datos.forEach(actividad => {
                        // Aplicamos el resaltado a los campos correspondientes 
                        const nombreResaltado = resaltarTexto(actividad.nombreActividad, textoBusqueda);
                        const descripcionResaltada = resaltarTexto(actividad.descripcion, textoBusqueda);
                        const comunaResaltada = resaltarTexto(actividad.comuna, textoBusqueda);

                        // Creamos el contenedor de la tarjeta
                        const div = document.createElement('div');
                        div.classList.add('actividad-card'); 

                        // Construimos el HTML interno 
                        div.innerHTML = `
                            <h3>${nombreResaltado}</h3>
                            <p><strong>Descripción:</strong> ${descripcionResaltada}</p>
                            <ul>
                                <li><strong>Miembro asociado:</strong> ${actividad.nombreMiembro}</li>
                                <li><strong>Día:</strong> ${actividad.dia}</li>
                                <li><strong>Tipo:</strong> ${actividad.tipo}</li>
                                <li><strong>Comuna:</strong> ${comunaResaltada}</li>
                            </ul>
                            
                            <div class="evaluacion-seccion">
                                <p><strong>Nota actual:</strong> <span id="nota-texto-${actividad.id}">${actividad.nota}</span></p>
                                
                                <div class="form-evaluar">
                                    <label for="input-nota-${actividad.id}">Evaluar (1-7):</label>
                                    <input type="number" id="input-nota-${actividad.id}" min="1" max="7" step="1">
                                    <button onclick="enviarEvaluacion(${actividad.id})">Evaluar</button>
                                </div>
                            </div>
                            <hr>
                        `;

                        contenedorResultados.appendChild(div);
                    });
                })
                .catch(error => {
                    console.error("Error fetching data:", error);
                    contenedorResultados.innerHTML = "<p>Error al buscar las actividades.</p>";
                });
        } else {
            contenedorResultados.innerHTML = "<p>Comienza a escribir para ver los resultados...</p>";
        }
    });
});