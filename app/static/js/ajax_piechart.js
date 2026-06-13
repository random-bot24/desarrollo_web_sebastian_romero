function procesarDatos2(datos){
    const datosListos = datos.map((actividad) => {
        const tipoActividad = actividad.tipo;
        const cantidad = actividad.cantidad;
        return [tipoActividad, cantidad];
    })
    return datosListos;
}

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

async function createPieChart(){
    try{
        const data = await getData('http://127.0.0.1:5000/get-activities-per-type');
        const processedData = procesarDatos2(data);
        // code to create pie chart using processed data and Highcharts
        Highcharts.chart('container2', {
            chart: {
                type: 'pie',
            },
            title: {
                text: 'Distribución de Tipos de Actividades',
                style: {
                    fontSize: '20px',
                    color: '#333'
                }
            },
            tooltip: {
                pointFormat: '<b>{point.y}%</b>'
            },
            series: [{
             name: 'Actividades',
                colorByPoint: true,
                data: processedData
            }],
            credits: {
                enabled: false
            }
        });
    }
    catch(error){
        console.error('Error creating pie chart', error);
        document.getElementById('container').innerHTML = '<p>Error al cargar el gráfico</p>';
    }
}

createPieChart();