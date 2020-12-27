const questions = {}
const form = document.querySelector('#form-questions')

form.addEventListener('submit', event => submitForm(event, form))

function handleTypeQuestion(e){
    const {value, name} = e
    const splitPrefix = name.split('-')
    const idxQuestion = splitPrefix[0] + '-' + splitPrefix[1] + '-default_value' // Attr name do campo que guarda o default_value
    const inputDefVal = document.querySelector(`[name=${idxQuestion}]`) // Campo que guarda o default_value
    const parent = e.parentNode.parentNode.parentNode // Div raiz
    console.log(parent)
    const idDiv = `type_question-${idxQuestion}`

    inputDefVal.value = ''
    removeBlockTypeQuestion(idxQuestion)
    
    if (value == 'MULTI_CHOICE' || value == 'CHECKBOXES'){
        //questions[idxQuestion] = []
        createBlockAlternatives(parent, idxQuestion)
        hidenInputDefVal(inputDefVal)
    }
    else if (value == 'TRUE_FALSE'){
        createBlockTrueFalse(parent, idxQuestion)
        hidenInputDefVal(inputDefVal)
    }
    else if (value == 'TEXT'){
        showInputDefVal(inputDefVal)
    }
}

function removeQuestion(idxQuestion){
    const input = document.querySelector(`[name='${idxQuestion}']`)

    if (input){
        const div = document.querySelector(`div[data-input-block='${idxQuestion}']`)
        input.value = ''
        
        if (div){
            div.remove()
        }
    }
}

function createBlockTypeQuestion(parent, idDiv, aditionalClasses=[]){
    const div = document.createElement('div')

    aditionalClasses.forEach(_class => {
        div.classList.add(_class)
    })

    div.classList.add('col-md-12','mb-3')
    div.setAttribute('data-input-block', idDiv)

    parent.insertBefore(div, parent.lastElementChild)
    //parent.appendChild(div)

    return div
}

function removeBlockTypeQuestion(idxQuestion){
    const div = document.querySelector(`div[data-input-block='${idxQuestion}']`)
    console.log(div)
    if (div){
        //delete questions[idxQuestion]
        div.remove()
    }
}

function createBlockAlternatives(parent, idxQuestion){
    const div = createBlockTypeQuestion(parent, idxQuestion)
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
    btnDeleteInput.innerHTML = 'Apagar'
    btnDeleteInput.type = 'button'
    
    newInput.placeholder = 'Alternativa'
    newInput.setAttribute('data-input-alternative', idxQuestion)

    // Função para apagar alternativa
    btnDeleteInput.addEventListener('click', () => {
        removeAlternative(row, newInput, idxQuestion)
        console.log(questions)
    })

    
    divInput.append(newInput)
    row.append(divInput, btnDeleteInput)

    //questions[idxQuestion].push(newInput)
    console.log(questions)

    divRoot.insertBefore(row, divRoot.lastElementChild)

    return row
}

function removeAlternative(nodeRow, input, idxQuestion){
    //questions[idxQuestion] = questions[idxQuestion].filter(alternative => alternative != input)

    nodeRow.remove()
}

function createBlockTrueFalse(parent, idxQuestion, idDiv){
    const div = createBlockTypeQuestion(parent, idxQuestion)
    const divInput = document.createElement('div')
    const labelDiv = document.createElement('label')
    const input = document.createElement('input')
    const label = document.createElement('label')

    divInput.classList.add('form-check', 'form-switch')

    labelDiv.classList.add('mb-1', 'mt-1')
    labelDiv.innerHTML = 'Valor Padrão'

    input.classList.add('form-check-input')
    input.type = 'checkbox'
    input.id = `checkbox-${idxQuestion}`
    input.setAttribute('data-input-boolean', idxQuestion)

    input.addEventListener('change', () => {
        handleCheckbox(input, label, idxQuestion)
    })

    label.classList.add('form-check-label')
    label.htmlFor = `checkbox-${idxQuestion}`
    label.innerHTML = 'Falso'

    divInput.append(input, label)
    div.append(labelDiv, divInput)

    const inputDefVal = document.querySelector(`[name='${idxQuestion}']`)
    inputDefVal.value = input.checked

    return div
}

function handleCheckbox(checkBox, label, idxQuestion){
    const inputDefVal = document.querySelector(`[name='${idxQuestion}']`)
    
    if (checkBox.checked)
        label.innerHTML = 'Verdadeiro'  
    else
        label.innerHTML = 'Falso'

    inputDefVal.value = checkBox.checked
}

function hidenInputDefVal(el){
    el.parentNode.parentNode.classList.add('d-none')
}

function showInputDefVal(el){
    el.parentNode.parentNode.classList.remove('d-none')
}

/*function serializeAlternatives(){
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
}*/

function serializeAlternatives(){
    const inputs = document.querySelectorAll("[name*=default_value]")

    inputs.forEach(input => {
        const alternatives = document.querySelectorAll(`input[data-input-alternative='${input.name}']`)

        if (alternatives.length > 0){
            var alternativesSerialized = ''
    
            alternatives.forEach( (alternative, idx) => {
                if ( !(alternative.value.trim() == '')){
                    alternativesSerialized += alternative.value
    
                    if (idx < alternatives.length - 1)
                        alternativesSerialized += ';'
                }
            })

            input.value = alternativesSerialized
        }
    })

}

function submitForm(e, form){
    e.preventDefault()
    serializeAlternatives()
    form.submit()
}

