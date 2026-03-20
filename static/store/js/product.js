 const aTagFieldEl = document.getElementById('tag-add');
const helpTextEl = aTagFieldEl.dataset.help;
const divHelpEl = document.getElementById('help-container');

const aDeleteEl = document.getElementById('tag-delete')

aTagFieldEl.addEventListener('mouseenter', handleHover);
aTagFieldEl.addEventListener('mouseleave', handleLeave);

aDeleteEl.addEventListener('mouseenter', handleHoverDelete)
aDeleteEl.addEventListener('mouseleave', handleLeave)

function handleHover(){
    const smallHelpTextEl = document.createElement('small');
    smallHelpTextEl.classList.add('form-help');
    smallHelpTextEl.textContent = helpTextEl;

    divHelpEl.appendChild(smallHelpTextEl)
}

function handleLeave(){
    divHelpEl.innerHTML = '';
}

function handleHoverDelete(){
    const smallHelpTextEl = document.createElement('small');
    smallHelpTextEl.classList.add('form-help');
    smallHelpTextEl.textContent = 'delete tag/s';

    divHelpEl.appendChild(smallHelpTextEl)
}