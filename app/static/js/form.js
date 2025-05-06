
const formNoise = document.getElementById('formNoise');
const media = document.getElementById('media');
const deviation = document.getElementById('deviation');
const variance = document.getElementById('variance');

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

