if (navigator.mediaDevices.getUserMedia){
    const video = document.querySelector('#videoCam')
    navigator.mediaDevices.getUserMedia({ 
        video: {
            facingMode: 'user'
        }
    })
    .then(function (stream){
        video.srcObject = stream
        video.play()
    })
    .catch(function (err) {
        console.log('ERRO')
    })
}