function showToast(toastId, titulo, msg) {
    const toast = document.getElementById(toastId);
    toast.innerHTML = `<div class="bg-white shadow-lg rounded-lg p-4">
        <div class="flex items-center justify-between">
            <span class="font-bold">${titulo}</span>
            <button type="button" class="text-gray-500 hover:text-gray-600 focus:outline-none focus:text-gray-600" onclick="hideToast()">X</button>
        </div>
        <p class="text-sm text-gray-500 mt-2">${msg}</p>
    </div>`
    toast.classList.add('opacity-100');

    setTimeout(function() {
        toast.innerText = ''
        toast.classList.remove('opacity-100');
    }, 4000);
}

function previewFoto(e, elementPreview){
    const archivo = e.target.files[0];  
    const url = URL.createObjectURL(archivo);
    
    elementPreview.src = url;
}

const randomHexColor = () => {
    const part = () =>
      Math.floor(Math.random() * 256)
        .toString(16)
        .padStart(2, '0');

    const r = part(), g = part(), b = part();
    return `#${r}${g}${b}`;
};

function getUrlArgs(){
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    const args = {};
    for (const [key, value] of urlParams.entries()) 
        args[key] = value;

    return args
}

function formDataToObject(formData) {
    const entries = [...formData.entries()];
    return Object.fromEntries(entries.map(([key, value]) => [key, value]));
}

function validarLimpiarFormData(formData){
    const data = new FormData()
    for([key, val] of formData){
        let nuevo_val = val
        try{
            nuevo_val  = val.trim()
        } catch { }
        
        if(!nuevo_val || val.length === 0) return false
        data.append(key, nuevo_val)
    }
    return data
}

function divFinanciamiento(div){
    let temp = `
    <div class="flex flex-wrap px-2">
        <label class="w-full text-xl">Descripcion de la oferta</label>
        <textarea class="w-full p-2" name="descripcion" cols="30" rows="10"></textarea>
    </div>
    <div class="flex flex-wrap px-2">
        <div class="w-full h-1/3 m-0 flex items-center justify-center">
            <p class="w-1/3">Porcentaje de participaci&oacute;n</p>
            <input id="porcentaje" name="porcentaje" class="w-16 text-right border border-gray-300 rounded-l-lg px-2 py-1 focus:outline-none" type="number" min="1" max="99">
            <span class="bg-gray-100 border border-l-0 border-gray-300 rounded-r-lg px-2 py-1 text-gray-600">%</span>
        </div>
        <div class="w-full flex items-center justify-center">
            <label class="mr-2 text-md">Opcion de cr&eacute;dito</label>
            <input type="checkbox" name="conCredito" id="addCredito">
        </div>
    </div>`
    const divCredito = document.createElement('div')
    divCredito.classList.add('hidden', 'w-1/3', 'p-4', 'grid', 'grid-cols-2', 'gap-4')
    divCredito.innerHTML = `<div>
        <label for="credito" class="block font-bold mb-2">Crédito:</label>
        <input type="number" id="credito" name="credito" placeholder="Monto del crédito" class="w-full p-2 border rounded-md">
    </div>
    <div>
        <label for="interesCredito" class="block font-bold mb-2">Tasa de Interés:</label>
        <input type="number" id="interesCredito" name="interesCredito" placeholder="Tasa de interés" class="w-full p-2 border rounded-md">
    </div>`
    
    div.innerHTML = temp
    div.appendChild(divCredito)
    const checkAddCredito = div.querySelector('[id="addCredito"]')
    checkAddCredito.addEventListener('change', ()=> divCredito.classList.toggle('hidden'))

}