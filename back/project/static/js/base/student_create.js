function toggleNickFields() {
    const nickFields = document.querySelectorAll('.nick')

    nickFields.forEach(field => {
        field.classList.toggle('d-none')
    })
}

function toggleStep(action, currentStep, validate=false){
    const pass = action === 'next' ? 1 : -1
    var allValid = false

    if (validate){
        allValid = validateFields(currentStep)
    }
    
    if (!validate || allValid){
        const tab = document.querySelector(`#tabs a[href="#tab-${currentStep}"]`)
        const otherTab = document.querySelector(`#tabs a[href="#tab-${currentStep + pass}"]`)
        const content = document.querySelector(`#steps div[id="tab-${currentStep}"]`)
        const otherContent = document.querySelector(`#steps div[id="tab-${currentStep + pass}"]`)
    
        if (tab && otherTab && content && otherContent){
            tab.classList.replace('active', 'disabled')
            otherTab.classList.replace('disabled', 'active')
        
            content.classList.remove('active', 'show')
            otherContent.classList.add('active', 'show')
        }
    }
}

function validateFields(currentStep){
    const inputs = document.querySelectorAll(`#tab-${currentStep} input, select, textarea`)

    for (var i=0; i < inputs.length; ++i){
        if (!inputs[i].reportValidity())
            return false
    }

    return true
}