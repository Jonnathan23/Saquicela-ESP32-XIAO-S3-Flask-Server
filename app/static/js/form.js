const urlStreamingGaussian = "/video_stream_b";
const urlFilterMaskLocal = "/photo_local_filters_mask";
const urlFilterMaskEsp = "/photo_esp_filters_mask";

//* Asignacion del DOM

// Formulario
const formNoise = document.getElementById('formNoise');
const media = document.getElementById('media');
const deviation = document.getElementById('deviation');
const variance = document.getElementById('variance');

// Botones
const btStreamingGaussian = document.getElementById('btStreamingGaussian');
const btPhotoMaskEsp = document.getElementById('btPhotoMaskEsp');
const btPhotoMaskLocal = document.getElementById('btPhotoMaskLocal');

// Streaming/ Foto
const imageStreamingGaussian = document.getElementById('streaming_image');
const imagePhotogMask = document.getElementById('PhotoMask');



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

const uniqueUrl = (url) => url + '?_=' + Date.now();

btStreamingGaussian.addEventListener('click', () => {
    imagePhotogMask.src = "#"

    imageStreamingGaussian.src = uniqueUrl(urlStreamingGaussian);
})

btPhotoMaskEsp.addEventListener('click', () => {
    alert('Tomando foto')
    imageStreamingGaussian.src = "#";
    imagePhotogMask.src = uniqueUrl(urlFilterMaskEsp);
})

btPhotoMaskLocal.addEventListener('click', () => {
    alert('Tomando foto')
    imageStreamingGaussian.src = "#";
    imagePhotogMask.src = uniqueUrl(urlFilterMaskLocal);
})