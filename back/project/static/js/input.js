const inputButtonClick = (id) => {
    const inputFile = document.querySelector(`input[id="${id}"]`)
    inputFile.click()
}

const inputChange = (e) => {
    const detail = document.querySelector('#details-file')
    detail.innerHTML = e.files.length + ' imagens selecionadas.'
}
