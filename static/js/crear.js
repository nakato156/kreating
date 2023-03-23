window.onload = init
window.onsubmit = (e) => e.preventDefault()

let ctx, myChart;
let imgProyecto, formProyecto;
let porcentaje;
let porcentajes = [100], participantes = ['Yo'];
let divFinanciacion;

function init(){
    ctx = document.getElementById('myChart').getContext('2d');
    porcentaje = document.getElementById('porcentaje')
    formProyecto = document.getElementById('formP')
    imgProyecto = document.getElementById('ft_proyect')
    divFinanciacion = document.getElementById('secFinanciacion')
    const nameList = document.getElementById('name-list');
    const addBtn = document.getElementById('add-btn');
    const nameInput = document.getElementById('name-input');
    const crearBtn = document.getElementById('crearP')
    const preview = document.getElementById('preview')
    const estadoProyecto = document.getElementById('status')

    addBtn.addEventListener('click', () => addUsuario(nameList, nameInput))
    crearBtn.addEventListener('click', crearProyecto)
    imgProyecto.addEventListener('change', (e) => previewFoto(e, preview))
    estadoProyecto.addEventListener('change', cuadroFinanciacion)
    
    myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: participantes,
            datasets: [{
                data: porcentajes,
                backgroundColor: ['#ff6384']
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

function updateChart() {   
    myChart.data.labels = participantes;
    myChart.data.datasets[0].backgroundColor.push(randomHexColor())
    myChart.data.datasets[0].data = porcentajes;
    myChart.update();
}

const addUsuario = (nameList, nameInput) => {
    const email = nameInput.value.trim();
    const percent = Number(porcentaje.value)

    if(email === MYEMAIL) return Swal.fire({
        'icon': 'info',
        'text': 'No puede agregarse nuevamente como fundador'
    })

    if(porcentajes[0] - percent < 1) return Swal.fire({
        'icon': 'error',
        'text':'Se sobrepasa el 100%'
    })

    if (email !== '' && 0 < percent && percent <= 99 ) {
        const li = document.createElement('li');
        li.classList.add('flex', 'items-center', 'justify-between', 'bg-gray-100', 'rounded-lg', 'px-2', 'py-1', 'mt-2');
        li.innerHTML =`
        <span class="text-gray-600">${percent}%</span>
        <span class="text-gray-800">${email}</span>
        <button class="text-red-500 hover:text-red-600" type="button">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>      
        </button>`;

        const yo = porcentajes[0] - percent
        porcentajes[0] = yo
        porcentajes.push(percent)
        participantes.push(email)

        const removeBtn = li.querySelector('button');
        removeBtn.addEventListener('click', () => {
            const usuario = li.children[1].innerHTML
            if(participantes.includes(usuario)) 
                li.remove() 
        });
        nameList.appendChild(li);
        nameInput.value = '';
        porcentaje.value = ''
        updateChart()
    }
};

function countWords() {
    const wordCount = document.getElementsByName("descripcion")[0].value.length;
    document.getElementById("wordCount").textContent = wordCount;
}

function crearProyecto(){
    const obj = participantes.reduce((acc, key, index) => ({...acc, [key]: porcentajes[index]}), {});
    const valuacion = Number(document.getElementById('valuacion').value)

    if (isNaN(valuacion)) return Swal.fire({'icon': 'error', 'title':'Valor de valuación incorrecta'})

    let cols = ''

    porcentajes.forEach((porcentaje, i) =>{
        const email = participantes[i] === 'Yo' ? MYEMAIL : participantes[i]
        cols += `<tr class="border-b dark:border-neutral-500">
            <td class="whitespace-nowrap  px-6 py-4 font-medium">${i + 1}</td>
            <td class="whitespace-nowrap  px-6 py-4 ">${porcentaje}</td>
            <td class="whitespace-nowrap  px-6 py-4">${email}</td>
        </tr>`
    })

    let temp_table = `<div class="flex flex-col">
        <div class="overflow-x-auto sm:-mx-6 lg:-mx-8">
            <div class="inline-block min-w-full py-2 sm:px-6 lg:px-8">
                <div class="overflow-hidden">
                    <table class="min-w-full text-center text-sm font-light">
                        <thead class="border-b bg-neutral-50 font-medium dark:border-neutral-500 dark:text-neutral-800">
                            <tr>
                                <th scope="col" class=" px-6 py-4">#</th>
                                <th scope="col" class=" px-6 py-4">Procentaje %</th>
                                <th scope="col" class=" px-6 py-4">Email</th>
                            </tr>
                        </thead>
                        <tbody>${cols}</tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>`

    Swal.fire({
        'title': 'Resumen',
        'html': temp_table,
        showCancelButton: true,
    })
    .then( result => {
        if(result.isConfirmed) {
            const data = {
                'valuacion': valuacion,
                'imagen': imgProyecto.files[0],
                data: JSON.stringify(obj)
            }

            const financiamiento = getInfoFinanciamiento()
            console.log(financiamiento)
            if(financiamiento) data['financiamiento'] = JSON.stringify(financiamiento)
            
            
            if(imgProyecto.files.length === 0) return Swal.fire({'icon': 'error', 'text': 'Escoja una imagen'})

            const formData = new FormData(formProyecto)
            for(const [key, val] of Object.entries(data)) formData.append(key, val);
            
            const new_data = validarLimpiarFormData(formData)
            if(new_data) enviarProyecto(new_data)
            else Swal.fire({'icon': 'error', 'title': 'Complete todos los datos'})
        }
    })
}

function enviarProyecto(payload){
    fetch('/crear-proyecto', {
        method: 'POST',
        body: payload
    })
    .then(req => req.json())
    .then(res => {
        if(res.error){
            return Swal.fire({'icon': 'error', 'text': res.error})
        }
        Swal.fire({'icon': 'success', 'title': 'Proyecto creado'})
        .then(res => location.href = '/perfil')
    })
}

function getInfoFinanciamiento(){
    const form = document.getElementById('formFinanciacion')
    if(form) return formDataToObject(new FormData(form))
    return false
}

function cuadroFinanciacion(e) {
    const element = e.target
    const valor = element.value

    if(valor === '2'){
        divFinanciacion.classList.remove('hidden')
        divFinanciamiento(divFinanciacion.firstElementChild)
    } else divFinanciacion.classList.add('hidden')
}