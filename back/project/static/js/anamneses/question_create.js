const questions = {}
const form = document.querySelector('#form-questions')

form.addEventListener('submit', event => submitForm(event, form))

function handleTypeQuestion(e){
    const {value, name} = e
    const splitPrefix = name.split('-')
    const idxQuestion = splitPrefix[0] + '-' + splitPrefix[1] + '-default_value' // Attr name do campo que guarda o default_value
    const inputDefVal = document.querySelector(`[name=${idxQuestion}]`) // Campo que guarda o default_value
    const parent = e.parentNode // Div raiz
    const idDiv = `type_question-${idxQuestion}`

    inputDefVal.value = ''
    removeBlockTypeQuestion(idDiv, idxQuestion)
    
    if (value == 'MULTI_CHOICE' || value == 'CHECKBOXES'){
        questions[idxQuestion] = []
        createBlockAlternatives(parent, idxQuestion, idDiv)
        hidenInputDefVal(inputDefVal)
    }
    else if (value == 'TRUE_FALSE'){
        createBlockTrueFalse(parent, inputDefVal, idxQuestion, idDiv)
        hidenInputDefVal(inputDefVal)
    }
    else if (value == 'TEXT'){
        showInputDefVal(inputDefVal)
    }
}

function removeQuestion(idxQuestion){
    delete questions[idxQuestion]
}

function createBlockTypeQuestion(parent, idDiv, aditionalClasses=[]){
    const div = document.createElement('div')

    aditionalClasses.forEach(_class => {
        div.classList.add(_class)
    })

    div.classList.add('mb-2', 'mt-2')
    div.id = idDiv

    parent.appendChild(div)

    return div
}

function removeBlockTypeQuestion(idDiv, idxQuestion){
    const div = document.querySelector(`#${idDiv}`)
    console.log(div)
    if (div){
        delete questions[idxQuestion]
        div.remove()
    }
}

function createBlockAlternatives(parent, idxQuestion, idDiv){
    const div = createBlockTypeQuestion(parent, idDiv)
    const btnAdd = document.createElement('button')

    btnAdd.classList.add('btn', 'btn-success', 'mt-2')
    btnAdd.innerHTML = 'Adicionar Alternativa'
    btnAdd.type = 'button'
    
    btnAdd.addEventListener('click', () => {
        createAlternative(div, idxQuestion)
    })

    div.append(btnAdd)

    createAlternative(div, idxQuestion)
}

function createAlternative(divRoot, idxQuestion){
    // Criando os elementos
    const row = document.createElement('div')
    const label = document.createElement('label')
    const divInput = document.createElement('div')
    const newInput = document.createElement('input')
    const btnDeleteInput = document.createElement('button')

    // Adicionando classes aos elementos
    row.classList.add('row', 'mb-2')
    label.classList.add('col-sm-2', 'col-form-label')
    divInput.classList.add('col-sm-6')
    newInput.classList.add('form-control')
    btnDeleteInput.classList.add('col-sm-2', 'btn', 'btn-danger')

    // Adicionando atributos aos elementos
    label.innerHTML = 'Alternativa'
    newInput.placeholder = 'Alternativa'
    btnDeleteInput.innerHTML = 'Apagar'
    btnDeleteInput.type = 'button'

    // Função para apagar alternativa
    btnDeleteInput.addEventListener('click', () => {
        removeAlternative(row, newInput, idxQuestion)
        console.log(questions)
    })

    
    divInput.append(newInput)
    row.append(divInput, btnDeleteInput)

    questions[idxQuestion].push(newInput)
    console.log(questions)

    divRoot.insertBefore(row, divRoot.lastElementChild)

    return row
}

function removeAlternative(nodeRow, input, idxQuestion){
    questions[idxQuestion] = questions[idxQuestion].filter(alternative => alternative != input)

    nodeRow.remove()
}

function createBlockTrueFalse(parent, inputDefVal, idxQuestion, idDiv){
    const div = createBlockTypeQuestion(parent, idDiv)
    const divInput = document.createElement('div')
    const labelDiv = document.createElement('label')
    const input = document.createElement('input')
    const label = document.createElement('label')

    divInput.classList.add('form-check', 'form-switch')

    labelDiv.classList.add('mb-1', 'mt-2')
    labelDiv.innerHTML = 'Valor Padrão'

    input.classList.add('form-check-input')
    input.type = 'checkbox'
    input.id = `checkbox-${idxQuestion}`

    input.addEventListener('change', () => {
        handleLabelTrueFalse(label, input, inputDefVal)
    })

    label.classList.add('form-check-label')
    label.htmlFor = `checkbox-${idxQuestion}`
    label.innerHTML = 'Falso'

    divInput.append(input, label)
    div.append(labelDiv, divInput)

    inputDefVal.value = input.checked

    return div
}

function handleLabelTrueFalse(label, checkBox, inputDefVal){
    const value = label.innerHTML
    
    if (value == 'Falso')
        label.innerHTML = 'Verdadeiro'  
    else if (value == 'Verdadeiro')
        label.innerHTML = 'Falso'

    inputDefVal.value = checkBox.checked
}

function hidenInputDefVal(el){
    el.parentNode.classList.add('d-none')
}

function showInputDefVal(el){
    el.parentNode.classList.remove('d-none')
}

function serializeAlternatives(){
    for (const [name, alternatives] of Object.entries(questions)){
        var alternativesSerialized = ''

        alternatives.forEach( (alternative, idx) => {
            if ( !(alternative.value.trim() == '')){
                console.log(alternative.value)
                alternativesSerialized += alternative.value

                if (idx < alternatives.length - 1)
                    alternativesSerialized += ';'
            }
        })

        const input = document.querySelector(`[name=${name}]`)
        input.value = alternativesSerialized
    }
}

function submitForm(e, form){
    console.log(questions)
    e.preventDefault()
    serializeAlternatives()
    form.submit()
}

