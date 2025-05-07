const urlStreamingLocal = '/video_stream_local'
const urlStreamingEsp32 = 'video_stream_esp32'

const options = {
    "0": "",
    "1": "AND",
    "2": "OR",
    "3": "XOR",
}

//* Elemntos DOOM

// Botones
const btEsp32 = document.getElementById('btEsp')
const btLocal = document.getElementById('btLocal')

// Image
const streamingImage = document.getElementById('streaming_image')

// Select
const cbOperations = document.getElementById('operations')

//* Eventos

btEsp32.addEventListener('click', () => setUrlStreaming('set-operation',urlStreamingEsp32))
btLocal.addEventListener('click', () => setUrlStreaming('set-operation',urlStreamingLocal))

const uniqueUrl = (url) => url + '?_=' + Date.now();

const setUrlStreaming = async (urlHttp, urlStreaming) => {
    const operations = cbOperations.value;

    fetch(urlHttp, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({            
            operations: options[operations]
        })
    })
    .then((data) =>{
        if(data.status === 200){
            alert('Implementando video')
            streamingImage.src = uniqueUrl(urlStreaming)
            return
        }

        alert('No ha seleccionado el metodo')
    })    
    .catch(() => alert('Error con el servidor'))
}