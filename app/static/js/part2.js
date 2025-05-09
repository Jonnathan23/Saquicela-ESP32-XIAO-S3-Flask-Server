const urlAxialBoneC = '/axial-bone-c-result';
const urlAxialBone = '/axial-bone-result';
const urlAxialBoneLung = '/axial-lung-result';

const typeSizeMorfologicalSizeKermels = {
    "0": "",
    "1": 15,
    "2": 37,
    "3": 55
}

const morfologicsOperations = {
    "0": "",
    "1": "erosion",
    "2": "dilation",
    "3": "topHat",
    "4": "blackHat",
    "5": "originalImageTopBlackHat",
}

// selects
const cbMorfologicsOperations = document.getElementById('morfologicsOperations');
const cbTypeSizeMorfologicalSizeKermels = document.getElementById('sizeMask');

// Buttons
const btApply = document.getElementById('btApply');

// Images
const imageAxialBoneC = document.getElementById('axial_bone_c+');
const imageAxialBone = document.getElementById('axial_bone');
const imageAxialBoneLung = document.getElementById('axial_lung');

//* Events Listeners

btApply.addEventListener('click', () => applyMorfologicalOperation());

const applyMorfologicalOperation = () => {
    const operation = cbMorfologicsOperations.value;
    const sizeMask = cbTypeSizeMorfologicalSizeKermels.value;

    fetch('/set-morfological-operations', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            operation: morfologicsOperations[operation],
            sizeMask: typeSizeMorfologicalSizeKermels[sizeMask]
        })
    })
        .then((data) => {
            if (data.status === 200) {
                alert('se guardaron los parametros de la mascara')
                imageAxialBoneC.src = urlAxialBoneC;
                imageAxialBone.src = urlAxialBone;
                imageAxialBoneLung.src = urlAxialBoneLung;

                return;
            }

            alert("No ha seleccionado todas las opciones")
        })
        .catch((error) => {
            alert("Error con el servidor")
            console.log(error)
        })
}