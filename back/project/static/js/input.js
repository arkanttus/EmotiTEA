const inputButtonClick = (id) => {
    const inputFile = document.querySelector(`input[id="${id}"]`)
    inputFile.click()
}

const inputChange = (e) => {
    const detail = document.querySelector('#details-file')

    detail.innerHTML = e.files.length + ' imagens selecionadas.'

    /*
    if(e.nextElementSibling.tagName == "INPUT"){
        e.nextElementSibling.value = e.files.length + ' imagens selecionados.'
    }
    else if(e.nextElementSibling.tagName == "BUTTON")
        e.nextElementSibling.style.filter = "brightness(100%)"
    */
}
