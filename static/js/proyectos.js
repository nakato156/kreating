window.onload = init

function init(){
    const proyectos = document.querySelectorAll('.cardPry')

    proyectos.forEach(proyecto => {
        proyecto.addEventListener('click', () => location.href = `/proyecto/${proyecto.id}`)
    })
}