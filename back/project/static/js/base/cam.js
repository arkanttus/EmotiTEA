var video = document.querySelector('#videoCam')

if (navigator.mediaDevices.getUserMedia){
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function (stream){
            video.srcObject = stream
        })
        .catch(function (err) {
            console.log('ERRO')
        })
}


function preprocess(imgData) {
    return tf.tidy(() => {
        let tensor = tf.browser.fromPixels(imgData).toFloat();

        tensor = tensor.resizeBilinear([100, 100]);

        tensor = tf.cast(tensor, "float32");
        const offset = tf.scalar(255.0);
        // Normalize the image
        const normalized = tensor.div(offset);
        //We add a dimension to get a batch shape
        const batched = normalized.expandDims(0);
        return batched;
    });
}

async function getImage(){
    const {width, height} = faceapi.getMediaDimensions(video)
    const result = await faceapi.detectSingleFace(video, new faceapi.TinyFaceDetectorOptions() )

    const canvas = document.querySelector('#overlay')
    canvas.width = width
    canvas.height = height

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0, width, height);
    
    var item = result.box
    let s_x = Math.floor(item._x + offset_x)

    if (item.y < offset_y) {
        var s_y = Math.floor(item._y)
    } else {
        var s_y = Math.floor(item._y - offset_y)
    }

    let s_w = Math.floor(item._width - offset_x)
    let s_h = Math.floor(item._height)
    let cT = ctx.getImageData(s_x, s_y, s_w, s_h)

    cT = preprocess(cT)

    play(cT)
}


async function play(img){
    console.log(urlModel)
    const model = await tf.loadLayersModel(urlModel)
    console.log(model)

    //model.inputs.shape = [48, 48, 1]
    //console.log(model)
    
    

    /*const vi = await tf.browser.fromPixels(video)
    vi = vi.reshape([1, 48, 48, 1])
    console.log(vi)*/
    
    const prediction = model.predict(img)
    console.log(prediction)
}

video.addEventListener('loadeddata', (e) => {
    getImage()
})
