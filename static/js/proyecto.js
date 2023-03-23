window.addEventListener('DOMContentLoaded', init)

function init(){
    const ctx = document.getElementById('myChart').getContext('2d');
    const modal = document.getElementById('modal');
    try { generarModal(modal, addEvento) } catch (error) {}

    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: participantes,
            datasets: [{
                data: porcentajes,
                backgroundColor: colors
            }]
        },
        options: {
            plugins: {
                legend: {
                    display: false
                },
            }
        }
    });
}

function addEvento(e){
    e.preventDefault()
    const formData = new FormData(e.target)
    const data = validarLimpiarFormData(formData)

    if(!data) return Swal.fire({icon:'error', text: 'Complete todos los campos'})

    fetch(`/add-evento/${ID}`, {
        method:'POST',
        body: data
    })
    .then( req => req.json())
    .then( res => {
        if(res.error){
            return Swal.fire({icon: 'eror', text: res.error})
        }
        Swal.fire({icon: 'succes', title: 'Evento agregado'})
    })
}

function callbackChecked(e){
    const element = e.target
    const contenedorInputs = e.target.parentNode.parentNode

    if(!element.checked){
        const inputEnlace = contenedorInputs.querySelector('[id="enlace"]')
        return contenedorInputs.removeChild(inputEnlace.parentNode)
    }

    const div = document.createElement('div')
    div.classList.add('mb-4');
    
    const inputEnlace = document.createElement('input')
    inputEnlace.name = 'enlace'
    inputEnlace.id = 'enlace'
    inputEnlace.classList.add('border', 'border-gray-400', 'w-full', 'p-2', 'rounded-lg')
    inputEnlace.placeholder = 'Ingrese el link de la reunion'
    
    div.appendChild(inputEnlace)
    
    const divBtn = contenedorInputs.querySelector('button').parentNode
    contenedorInputs.insertBefore(div, divBtn)
}