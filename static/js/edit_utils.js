const formFields = [
    { label: 'Nombre del evento', id: 'nombre', type: 'text' },
    { label: 'Descripción del evento', id: 'descripcion', element: 'textarea' },
    { label: 'Fecha del evento', id: 'fecha', type: 'date' },
    { label: 'Es virtual?', id:'tipo', type: 'checkbox', event:{
        name:'change',
        callback: callbackChecked
    }, styles:['w-6', 'h-6', 'border', 'border-gray-400'] }
];

const generarModal = (modal, callback) => {
    const backdrop = document.createElement('div');
    backdrop.classList.add('absolute', 'inset-0', 'bg-gray-500', 'opacity-75');
    modal.appendChild(backdrop);

    const dialog = document.createElement('div');
    dialog.classList.add('inline-block', 'align-bottom', 'bg-white', 'rounded-lg', 'text-left', 'overflow-hidden', 'shadow-xl', 'transform', 'transition-all', 'sm:my-8', 'sm:align-middle', 'sm:max-w-lg', 'sm:w-full');
    modal.appendChild(dialog);

    const content = document.createElement('div');
    content.classList.add('bg-white', 'px-4', 'pt-5', 'pb-4', 'sm:p-6', 'sm:pb-4');
    dialog.appendChild(content);

    const form = document.createElement('form');
    content.appendChild(form);

    // agregar los campos del formulario
    formFields.forEach( field => {
      const fieldDiv = document.createElement('div');
      fieldDiv.classList.add('mb-4');

      const fieldLabel = document.createElement('label');
      fieldLabel.classList.add('block', 'text-gray-700', 'font-bold', 'mb-2');
      fieldLabel.setAttribute('for', field.id);
      fieldLabel.textContent = field.label;

      const element = field.element ? field.element : 'input'
      const fieldInput = document.createElement(element);
      const styles = field.styles ? field.styles : ['form-input', 'border', 'border-gray-400', 'rounded-lg', 'p-2', 'w-full']
      fieldInput.classList.add(...styles);
      fieldInput.setAttribute('type', field.type);
      fieldInput.setAttribute('id', field.id);
      fieldInput.setAttribute('name', field.id);

      if(field.event){
        fieldInput.addEventListener(field.event.name, field.event.callback)
      }

      fieldDiv.appendChild(fieldLabel);
      fieldDiv.appendChild(fieldInput);
      form.appendChild(fieldDiv);
    });

    // agregar el botón para agregar evento
    const buttonDiv = document.createElement('div');
    buttonDiv.classList.add('mt-6');

    const addButton = document.createElement('button');
    addButton.classList.add('bg-green-500', 'hover:bg-green-600', 'text-white', 'font-bold', 'py-2', 'px-4', 'rounded', 'shadow');
    addButton.setAttribute('type', 'submit');
    addButton.textContent = 'Agregar evento';

    buttonDiv.appendChild(addButton);
    form.appendChild(buttonDiv);

    buttonDiv.appendChild(addButton);
    form.appendChild(buttonDiv);

    // agregar el botón para cerrar el modal
    const footer = document.createElement('div');
    footer.classList.add('bg-gray-50', 'px-4', 'py-3', 'sm:px-6', 'sm:flex', 'sm:flex-row-reverse');

    const closeButton = document.createElement('button');
    closeButton.classList.add('inline-flex', 'justify-center', 'w-full', 'rounded-md', 'border', 'border-transparent', 'px-4', 'py-2', 'bg-rose-600', 'text-base', 'leading-6', 'font-medium', 'text-white', 'shadow-sm', 'hover:bg-rose-700', 'focus:outline-none', 'focus:border-green-700', 'focus:shadow-outline-green', 'transition', 'ease-in-out', 'duration-150', 'sm:ml-3', 'sm:w-auto', 'sm:text-sm', 'sm:leading-5');
    closeButton.setAttribute('type', 'button');
    closeButton.textContent = 'Cancelar';
    
    footer.appendChild(closeButton);
    dialog.appendChild(footer);
    
    // agregar el modal al body
    document.body.appendChild(modal);

    const abrirModal = document.getElementById('abrir-modal');
    const cerrarModal = () => {
        modal.classList.add('hidden');
        modal.setAttribute('aria-hidden', 'true');
        modal.removeAttribute('style');
    };

    abrirModal.addEventListener('click', () => {
        modal.classList.remove('hidden');
        modal.setAttribute('aria-hidden', 'false');
        dialog.classList.remove('opacity-0');
        dialog.classList.add('opacity-100');
        backdrop.classList.remove('opacity-0');
        backdrop.classList.add('opacity-100');
        backdrop.classList.remove('pointer-events-none');
    });

    closeButton.addEventListener('click', cerrarModal);
    backdrop.addEventListener('click', cerrarModal);
    dialog.addEventListener('click', (e) => e.stopPropagation());
    form.addEventListener('submit', callback)
}