//functions to make charts with ajax
async function getData(url){
    const data = url;
    try{    
        const response = await fetch(data);
        if (!response.ok){
            throw new Error('error fetching data');
        }
        const jsonData = await response.json();
        return jsonData;
    }
    catch(error){
        console.error('Error obtaining data', error);
        throw error;
    }
}


function procesarDatos(datosFlask) {
  
  // Usamos .map() para transformar cada "diccionario" de la lista
  const datosListos = datosFlask.map((dia) => {
    
    // 1. Obtenemos el texto de la fecha usando el PUNTO: dia.fecha
    // y lo convertimos a milisegundos con Date() y getTime()
    const fechaEnMilisegundos = new Date(dia.fecha).getTime();
    
    // 2. Obtenemos la cantidad de usuarios usando el PUNTO: dia.nuevos_miembros
    const cantidad = dia.cantidad;
    
    // 3. Empaquetamos y retornamos los dos valores como [x, y]
    return [fechaEnMilisegundos, cantidad];
  });

  return datosListos;
}

function procesarDatos2(datos){
    const datosListos = datos.map((actividad) => {
        const tipoActividad = actividad.tipo;
        const cantidad = actividad.cantidad;
        return [tipoActividad, cantidad];
    })
    return datosListos;
}

//line chart shows the number of members registered for each day. X axis: days, Y axis: number of members
async function createlineChart(){
    try{
        const data = await getData('http://127.0.0.1:5000/get-register-per-day');
        const processedData = procesarDatos(data);
        // code to create line chart using processedData and Highcharts
        Highcharts.chart('container', {
            chart: {
                type: 'line',
            },
            title: {
                text: 'Número de Registrados por Día'
            },
            xAxis: {
                type: 'datetime',
                title: {
                    text: 'Fecha'
                }
            },
            yAxis: {
                title: {
                 text: 'Número de Registrados'
                }
            },
            series: [{
                name: 'Registrados',
                data: processedData,
                color: '#800080',
            }]
        });
    }
    catch(error){
        console.error('Error creating line chart', error);
        document.getElementById('container').innerHTML = '<p>Error al cargar el gráfico</p>';
    }
}

createlineChart();

