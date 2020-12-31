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