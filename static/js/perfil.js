window.onload = init

let btnGuardarCambios;

function init(){
    const preview = document.getElementById('preview')
    const inputFoto = document.getElementById('ft_perfil')
    const crearProyecto = document.getElementById('createProyect')
    const proyectos = document.querySelectorAll('.proyecto')
    const camposInfoUsuario = document.querySelectorAll('.userInfo')
    btnGuardarCambios = document.getElementById('btnActualizar')
    
    crearProyecto.addEventListener('click', () => location.href='/crear')
    inputFoto.addEventListener('change', (e) => previewFoto(e, preview))
    proyectos.forEach(proyecto => {
        proyecto.addEventListener('click', () => {
            const id = proyecto.getAttribute('data-id')
            location.href = `/proyecto/${id}`
        })
    })

    camposInfoUsuario.forEach(campo => {
        campo.addEventListener('change', ()=> btnGuardarCambios.classList.remove('hidden'))
    })
    btnGuardarCambios.addEventListener('click', () => guardarCambios(camposInfoUsuario))
}

function guardarCambios(campos){
    const data = new FormData()
    campos.forEach(campo => data.append(campo.name, campo.value))
    const foto_perfil = document.getElementById('ft_perfil')
    data.append('foto', foto_perfil.files[0])
    console.log(foto_perfil.files)

    fetch('/actualizar/info',{
        method: 'PUT',
        body: data
    })
    .then(req => req.json())
    .then(res => {
        const icon = res.error ? 'error' : 'success'
        Swal.fire({icon, text: res.msg})
        if(!res.error){
            btnGuardarCambios.classList.add('hidden')
        }
    })
}