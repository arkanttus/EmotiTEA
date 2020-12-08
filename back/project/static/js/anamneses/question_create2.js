const questions = {}

function getSelectedType(e){
    const {value, name} = e
    const splitPrefix = name.split('-')
    const prefix = splitPrefix[0] + '-' + splitPrefix[1]
    const nameInpDefVal = prefix + '-default_value'
    const inputDefVal = document.querySelector(`[name=${nameInpDefVal}]`)
    const parent = e.parentNode
    const rootNode = parent.parentNode

    if (value == 'MULTI_CHOICE' || value == 'CHECKBOXES'){
        questions[nameInpDefVal] = []

        removeTypeDiv(nameInpDefVal)

        const div = createTypeDiv(parent, nameInpDefVal)
        const btnAddAlternative = createBtnAlt(div, nameInpDefVal)

        hidenInputDefVal(inputDefVal)
    }

    console.log(prefix)
    console.log(nameInpDefVal)
}

function addRemoveQuestion(){

}

function hidenInputDefVal(el){
    el.parentNode.classList.add('d-none')
}

function removeTypeDiv(idxQuestion){
    const div = document.querySelector(`#alternatives-${idxQuestion}`)

    if (div)
        div.remove()
}

/*
    Cria uma div para armazenar as alternativas
*/
function createTypeDiv(parent, idxQuestion){
    const divRoot = document.createElement('div')
    

    divRoot.classList.add('mb-2', 'mt-2')
    divRoot.id = `alternatives-${idxQuestion}`
    
    parent.appendChild(divRoot)

    createAlternative(divRoot, idxQuestion)

    return divRoot
}

function createBtnAlt(div, idxQuestion){
    const btnAdd = document.createElement('button')

    btnAdd.classList.add('btn', 'btn-success', 'mt-2')
    btnAdd.innerHTML = 'Adicionar Alternativa'
    btnAdd.type = 'button'

    btnAdd.addEventListener('click', () => {
        createAlternative(div, idxQuestion)
    })

    div.append(btnAdd)

    return btnAdd
}

/*
    Cria uma alternativa e adiciona na div de alternativas
*/
function createAlternative(divRoot, idxQuestion){
    const row = document.createElement('div')
    const label = document.createElement('label')
    const divInput = document.createElement('div')
    const newInput = document.createElement('input')
    const btnDeleteInput = document.createElement('button')
    const idxAlternative = divRoot.childElementCount

    row.classList.add('row', 'mb-2')
    label.classList.add('col-sm-2', 'col-form-label')
    divInput.classList.add('col-sm-6')
    newInput.classList.add('form-control')
    btnDeleteInput.classList.add('col-sm-2', 'btn', 'btn-danger')

    label.innerHTML = 'Alternativa'
    newInput.placeholder = 'Alternativa'
    btnDeleteInput.innerHTML = 'Apagar'
    btnDeleteInput.type = 'button'

    btnDeleteInput.addEventListener('click', () => {
        removeAlternative(row, newInput, idxQuestion)
        console.log(questions)
    })

    divInput.append(newInput)

    row.append(divInput, btnDeleteInput)

    questions[idxQuestion].push(newInput)
    console.log(questions)

    divRoot.insertBefore(row, divRoot.lastElementChild)
}

function removeAlternative(nodeRow, input, idxQuestion){
    const restAlternatives = questions[idxQuestion].filter(alternative => alternative != input)
    
    questions[idxQuestion] = restAlternatives
    nodeRow.remove()
}

function serializeAlternative(){
    for (const [key, alternative] of Object.entries(alternatives)){
        if ( !(alternative.value.trim() == '')){
            console.log(alternative.value)
        }
    }
}

function updateDefaultValue(val, inputDefVal){
    inputDefVal.value = val
}

function copyAttrs(target, src){
    [...src.attributes].forEach(attr => {
        target.setAttribute(attr.nodeName, attr.nodeValue)
    })
}