async function cargarComentarios(idActividad) {
  try {
    const respuesta = await fetch(`/actividades/${idActividad}`);
    if (!respuesta.ok) throw new Error("No se pudieron obtener los comentarios");
    
    const comentarios = await respuesta.json();
    
    const contenedor = document.getElementById(`comentarios-container-${idActividad}`);
    contenedor.innerHTML = ""; 
    
    comentarios.forEach(c => {
      const fechaBonita = new Date(c.fecha).toLocaleDateString();
      contenedor.innerHTML += `
        <div class="comentario">
          <strong>${c.nombre}</strong> (${fechaBonita}): <p>${c.texto}</p>
        </div>
      `;
    });
    
  } catch (error) {
    console.error("Error en AJAX:", error);
  }
}

async function agregarComentario(evento, idActividad) {
    evento.preventDefault(); // evita que la pagina  recargue

    const inputNombre = document.getElementById(`nombre-${idActividad}`);
    const inputTexto = document.getElementById(`texto-${idActividad}`);
    const divError = document.getElementById(`mensaje-error-${idActividad}`);

    const nombre = inputNombre.value.trim();
    const texto = inputTexto.value.trim();

    if (nombre.length < 3 || nombre.length > 80) {
        divError.textContent = "El nombre debe tener entre 3 y 80 caracteres.";
        divError.style.display = "block";
        return;
    }
    if (texto.length < 5) {
        divError.textContent = "El comentario debe tener al menos 5 caracteres.";
        divError.style.display = "block";
        return;
    }

    
    divError.style.display = "none";

    try {
        const respuesta = await fetch(`/comentario/${idActividad}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre, texto: texto })
        });

        const resultado = await respuesta.json();
        if (!respuesta.ok) {
            divError.textContent = resultado.error || "Hubo un error en el servidor.";
            divError.style.display = "block";
        } else {
            divError.style.display = "none";
        
            document.getElementById(`form-comentario-${idActividad}`).reset();
        
            cargarComentarios(idActividad); 
        }

    } catch (error) {
        divError.textContent = "Error de conexión con el servidor.";
        divError.style.display = "block";
    }
}