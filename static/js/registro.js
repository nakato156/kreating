document.getElementById('form').addEventListener('submit', toggleError)

function toggleError(e) {
    e.preventDefault()
    
    const data = new FormData(this)

    for(let el of data) {
        const name = el[0], val = el[1];
        const element = this.querySelector(`[name=${name}]`).parentNode
        
        if(!val.trim()){
            element.querySelector('#error').classList.toggle('hidden')
            const allBorders = element.querySelector('.border-gray-200')
            const allTexts = element.querySelector('.text-gray-500')

            allBorders.classList.toggle('border-red-600')
            allTexts.classList.toggle('text-red-600')
            return
        }
    }

    fetch('/registro', {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formDataToJSON(data))
    })
    .then(req => req.json())
    .then(res => {
        if(res.error){
            showToast('toast', 'error', res.mensaje)
        }
    })
}

function formDataToJSON(data){
    json = {}
    for([key, val] of data) json[key] = val.trim()
    return json
}