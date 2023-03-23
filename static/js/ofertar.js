window.addEventListener('DOMContentLoaded', ()=>{
    const crearOfertaRadio = document.getElementById("crear-oferta");
    const formOferta = document.getElementById('formOferta')
    const btnAceptarOferta = document.getElementById('btnAceptarOferta')

    crearOfertaRadio.addEventListener("change", function() {
        if (crearOfertaRadio.checked) formOferta.classList.remove('hidden')
        else formOferta.classList.add('hidden')
        btnAceptarOferta.classList.toggle('hidden')
    });
    btnAceptarOferta.addEventListener('click', ()=> enviarOferta({'status': true}))
    formOferta.addEventListener('submit', ()=> enviarOferta(new FormData(formOferta)) )
})

function enviarOferta(data){
    fetch('/aceptar-oferta', {
        method: 'POST',
        body: data
    })
    .then(req => req.json())
    .then(res => console.log(res))
}