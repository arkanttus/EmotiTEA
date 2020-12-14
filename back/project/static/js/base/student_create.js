function toggleNickFields() {
    const nickFields = document.querySelectorAll('.nick')

    nickFields.forEach(field => {
        field.classList.toggle('d-none')
    })
}