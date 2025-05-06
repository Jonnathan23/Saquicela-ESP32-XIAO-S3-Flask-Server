const urlStreamingGaussian = "/video_stream_b";
const urlFilterMask = "/video_filters_mask";

// Formulario
const formNoise = document.getElementById('formNoise');
const media = document.getElementById('media');
const deviation = document.getElementById('deviation');
const variance = document.getElementById('variance');

// Streaming
const imageStreamingGaussian = document.getElementById('streaming_image');
const imageStreamingMask = document.getElementById('streamingMask');

// Botones
const btStreamingGaussian = document.getElementById('btStreamingGaussian');
const btStreamingMask = document.getElementById('btStreamingMask');

//* Eventos

// Formulario
formNoise.addEventListener('submit', async (e) => {
    e.preventDefault();
    const mediaValue = media.value;
    const deviationValue = deviation.value;
    const varianceValue = variance.value;

    fetch('/save-noise', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            media: mediaValue,
            deviation: deviationValue,
            variance: varianceValue
        })
    })
        .then((data) => data.status === 200 ? alert('se guardaron los parametros de ruido') : alert("Datos vacios o invalidos"))
        .catch((error) => alert("Error con el servidor"))
})

// Botones
btStreamingGaussian.addEventListener('click', () => {        
    imageStreamingMask.src = "#";    
    imageStreamingGaussian.src = urlStreamingGaussian;
})

btStreamingMask.addEventListener('click', () => {
    imageStreamingGaussian.src = "#";
    imageStreamingMask.src = urlFilterMask;
})