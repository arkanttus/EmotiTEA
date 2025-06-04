async function loadModels() {
    // Carregando o modelo para facial detection
    modelFace = await blazeface.load();

    // Carregando o modelo para emotion recognition
    model = await tf.loadLayersModel(urlModel)
}

function process_img(img) {
    return tf.tidy(() => {
        // Transforma a imagem em um tensor de pixels e diminui seu tamanho para 48x48
        const tensorI = tf.browser.fromPixels(img, 1).resizeBilinear([48, 48])
        const tensor = tf.cast(tensorI, "float32")

        // Offset para normalizar a imagem. 255 por causa das cores rgb
        const offset = tf.scalar(255.0)

        // Normalizando a imagem
        const normalized = tensor.div(offset)

        // Adicionando mais uma dimensão ao tensor da imagem, para ficar com o
        // esperado shape[1, W, H, 1]
        return normalized.expandDims(0)
    })
}

async function detectFaces() {

    var canvas = document.getElementById('overlay'),
        canvas_out = document.getElementById('output'),
        ctx_out,
        ctx

    const width = video.clientWidth
    const height = video.clientHeight

    // Canvas para desenhar o rosto
    canvas.setAttribute('width', `${width}px`)
    canvas.setAttribute('height', `${height}px`)
    ctx = canvas.getContext('2d')

    // Canvas para capturar os frames do video
    canvas_out.setAttribute('width', `${width}px`)
    canvas_out.setAttribute('height', `${height}px`)
    ctx_out = canvas_out.getContext('2d')

    const returnTensors = true;
    const annotateBoxes = false

    if (video.readyState >= 3) {
        predictions = await modelFace.estimateFaces(video, returnTensors, false, false);

        if (predictions.length > 0) {

            for (let i = 0; i < 1; i++) {
                if (returnTensors) {
                    predictions[i].topLeft = predictions[i].topLeft.arraySync();
                    predictions[i].bottomRight = predictions[i].bottomRight.arraySync();
                    if (annotateBoxes) {
                        predictions[i].landmarks = predictions[i].landmarks.arraySync();
                    }
                }

                // Regra de três para compensar a diferença do tamanho de video capturado e tamanho de video esperado
                const start = predictions[i].topLeft;
                start[0] = (start[0] * width) / video.videoWidth
                start[1] = (start[1] * height) / video.videoHeight

                const end = predictions[i].bottomRight;
                end[0] = (end[0] * width) / video.videoWidth
                end[1] = (end[1] * height) / video.videoHeight

                // Subtração entre os eixos X e Y para obter largura e altura
                const size = [end[0] - start[0], end[1] - start[1]];

                // Desenha o retangulo verde ao redor do rosto detectado
                ctx.strokeStyle = 'green'
                ctx.lineWidth = '4'
                ctx.rect(start[0], start[1], size[0], size[1]);
                ctx.stroke()

                // Desenha o frame de video atual no canvas e obtem a imagem
                ctx_out.drawImage(video, 0, 0, width, height);
                const pimg = ctx_out.getImageData(start[0], start[1], size[0], size[1])

                // Pré processamento da imagem, para poder ser classificada
                const img = process_img(pimg)

                await predict(img)
            }
        }
    }

    // Redesenha o canvas muitas vezes por segundo, de forma otimizada
    window.requestAnimationFrame(detectFaces)
}

function drawEmotions(result) {
    const emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

    // Atualizando as barras de emoções
    emotions.forEach((emot, index) => {
        const bar = document.querySelector(`#${emot}`)

        if (bar) {
            const value = Math.round((result[index] + Number.EPSILON) * 100)
            bar.innerHTML = `${value}%`
            bar.style.width = `${value}%`
        }
    })
}

async function predict(img) {
    const prediction = model.predict(img)
    const arr = prediction.arraySync()

    drawEmotions(arr[0])
}
