const urlStreamingGaussian = "/video_stream_b";
const urlFilterMaskLocal = "/photo_local_filters_mask";
const urlFilterMaskEsp = "/photo_esp_filters_mask";

const options = {
    "0": "",
    "1": "AND",
    "2": "OR",
    "3": "XOR",
}

const filterOptions = {
    "0": "",
    "1": "median",
    "2": "blur",
    "3": "gaussian",
    "4": "noOne",
}

const bordersDetectionOptios = {
    "0": "",
    "1": "Sobel",
    "2": "Candy", 
}

//* Asignacion del DOM

// Formulario
const formNoise = document.getElementById('formNoise');
const media = document.getElementById('media');
const deviation = document.getElementById('deviation');
const variance = document.getElementById('variance');

// Inputs
const maskWidth = document.getElementById('maskWidth');
const maskHeight = document.getElementById('maskHeight');
const kernel = document.getElementById('kernel')

//Select
const cbFilter = document.getElementById('filterOptions');
const cbBorderDetection = document.getElementById('bordersDetection')

// Botones
const btStreamingGaussian = document.getElementById('btStreamingGaussian');
const btPhotoMaskEsp = document.getElementById('btPhotoMaskEsp');
const btPhotoMaskLocal = document.getElementById('btPhotoMaskLocal');

// Streaming
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

btPhotoMaskEsp.addEventListener('click', () => setValues('/set-mask-values', urlFilterMaskEsp))
btPhotoMaskLocal.addEventListener('click', () => setValues('/set-mask-values',urlFilterMaskLocal))

const setValues = (urlHttp, urlFilterMask) => {
    const maskWidthValue = maskWidth.value;
    const maskHeightValue = maskHeight.value;
    const filterSelected = cbFilter.value
    const borderSelected = cbBorderDetection.value
    const kernelValue = kernel.value

    fetch(urlHttp, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            maskWidth: maskWidthValue,
            maskHeight: maskHeightValue,
            filterSelected: filterOptions[filterSelected],
            borderSelected: bordersDetectionOptios[borderSelected],
            kernelValue: kernelValue
        })
    })
        .then((data) => {
            if (data.status === 200) {
                imageStreamingGaussian.src = "#";
                imagePhotogMask.src = uniqueUrl(urlFilterMask);
                alert('se guardaron los parametros de la mascara')
            } else {
                alert("Datos vacios o invalidos")
            }
        })
        .catch((error) => alert("Error con el servidor"))
}