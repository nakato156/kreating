window.onload = init

function init(){
    const form = document.getElementById('form')
    form.addEventListener('submit', login)
}

function login(e){
    e.preventDefault()

    const data = new FormData(this)

    fetch('/login', {
        method: 'POST',
        body: data
    })
    .then(req => req.json())
    .then(res => {
        console.log(res)
        if(res.status){
            const redir = getUrlArgs().redir
            if(redir)
                return location.href = `/${redir}`
            location.href = '/perfil'
        }
    })
}