const urlStreamingGaussian = "/video_stream_b";
const urlFilterMaskLocal = "/photo_local_filters_mask";
const urlFilterMaskEsp = "/photo_esp_filters_mask";

const options = {
    "0": "",
    "1": "AND",
    "2": "OR",
    "3": "XOR",
}

//* Asignacion del DOM

// Formulario
const formNoise = document.getElementById('formNoise');
const media = document.getElementById('media');
const deviation = document.getElementById('deviation');
const variance = document.getElementById('variance');

//Mascara
const maskWidth = document.getElementById('maskWidth');
const maskHeight = document.getElementById('maskHeight');

//Select
const maskOperation = document.getElementById('maskOperation');

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
    const maskWidthValue = maskWidth.value;
    const maskHeightValue = maskHeight.value;    

    fetch('/set-mask-values', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maskWidth: maskWidthValue,
            maskHeight: maskHeightValue,            
        })
    })
        .then((data) => {
            if (data.status === 200) {
                imageStreamingGaussian.src = "#";
                imagePhotogMask.src = uniqueUrl(urlFilterMaskLocal);
                alert('se guardaron los parametros de la mascara')
            } else {
                alert("Datos vacios o invalidos")
            }
        })
        .catch((error) => alert("Error con el servidor"))

    imageStreamingGaussian.src = "#";
    imagePhotogMask.src = uniqueUrl(urlFilterMaskEsp);
})



btPhotoMaskLocal.addEventListener('click', () => {
    const maskWidthValue = maskWidth.value;
    const maskHeightValue = maskHeight.value;        

    fetch('/set-mask-values', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maskWidth: maskWidthValue,
            maskHeight: maskHeightValue,            
        })
    })
        .then((data) => {
            if (data.status === 200) {
                imageStreamingGaussian.src = "#";
                imagePhotogMask.src = uniqueUrl(urlFilterMaskLocal);
                alert('se guardaron los parametros de la mascara')
            } else {
                alert("Datos vacios o invalidos")
            }
        })
        .catch((error) => alert("Error con el servidor"))


})