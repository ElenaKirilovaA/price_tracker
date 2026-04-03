const BASE_URL = '/store/api/';
let currentId = null;
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const titleInputEl = document.getElementById('title');
const URLInputEl = document.getElementById('url');
const addBtnEl = document.getElementById('add-btn');
const loadBtnEl = document.getElementById('load-btn');
const editBtnEl = document.getElementById('edit-btn');

const sectionCardContainerEl = document.getElementById('store-card')

loadBtnEl.addEventListener('click', handleLoadBtn);
addBtnEl.addEventListener('click', handleAddBtn);
editBtnEl.addEventListener('click', handleEditBtn);

async function handleLoadBtn() {
    let res = await fetch(BASE_URL, { credentials: 'same-origin' })
    let data = await res.json()
    let dataInfo = Object.values(data)

// {id: 1, title: 'FakeStoreApi', created_at: '2026-03-19T19:32:50.475000Z', url: 'https://fakestoreapi.com/'}
    sectionCardContainerEl.innerHTML = ''

    dataInfo.forEach(obj => {
        const divCardEl = document.createElement('div');
        divCardEl.classList.add('card');

        const titleH2El = document.createElement('h2');
        titleH2El.textContent = obj.title;

        const pUrlEl = document.createElement('p');

        const spanUrlEl = document.createElement('span');
        spanUrlEl.classList.add('material-icons');
        spanUrlEl.textContent = 'link';


        const aUrlEl = document.createElement('a');
        aUrlEl.href = obj.url;
        aUrlEl.textContent = obj.url;

        const pCreatedAtEl = document.createElement('p');
        const strongDateEl = document.createElement('strong');
        strongDateEl.textContent = `created: ${obj.created_at}`;

        const changeBtnEl = document.createElement('button');
        changeBtnEl.classList.add('btn');
        changeBtnEl.textContent = 'Change';

        const deleteBtnEl = document.createElement('button');
        deleteBtnEl.type = 'button'; // 👈 ТОВА Е FIX-ЪТ
        deleteBtnEl.classList.add('btn', 'btn-danger');
        deleteBtnEl.textContent = 'Delete';

        pUrlEl.appendChild(spanUrlEl);
        pUrlEl.appendChild(aUrlEl);


        pCreatedAtEl.appendChild(strongDateEl);

        divCardEl.appendChild(titleH2El);
        divCardEl.appendChild(pUrlEl);
        divCardEl.appendChild(pCreatedAtEl);
        divCardEl.appendChild(changeBtnEl);
        divCardEl.appendChild(deleteBtnEl);

        sectionCardContainerEl.appendChild(divCardEl);

        changeBtnEl.addEventListener('click', handleChangeBtn)
        deleteBtnEl.addEventListener('click', handleDeleteBtn)

        function handleChangeBtn() {
            titleInputEl.value = obj.title;
            URLInputEl.value = obj.url;


            editBtnEl.disabled = false;
            addBtnEl.disabled = true;

            currentId = obj.id;
        }
        async function handleDeleteBtn() {
            const isConfirmed = confirm(`Are you sure you want to delete ${obj.title}`);

            if (!isConfirmed){
                return;
            }

            const response = await fetch(`${BASE_URL}${obj.id}/`, {
                method: 'DELETE',
                headers: {'X-CSRFToken': csrfToken}
            });

            if (!response.ok) {
                alert('Error deleting item');
             return;
            }

            await handleLoadBtn();
        }

    })

}

async function handleAddBtn(e) {
    e.preventDefault();
    const title = titleInputEl.value.trim();
    const url = URLInputEl.value.trim();

    if (!title || !url) return;

    const headers = {
        'Content-Type': 'application/json'
    };
    if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
    }

    await fetch(BASE_URL, {
    method: 'POST',
    headers: headers,
    body: JSON.stringify({ title, url }),
    credentials: 'same-origin'
    });

    titleInputEl.value = '';
    URLInputEl.value = '';

    await handleLoadBtn();
}


async function handleEditBtn(e) {
    e.preventDefault();

    const title = titleInputEl.value.trim();
    const url = URLInputEl.value;

    if (!title || !url){
        return;
    }
    const headers = {
        'Content-Type': 'application/json'
    };
    if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
    }
    await fetch(`${BASE_URL}${currentId}/`, {
        method: 'PATCH',
        headers: headers,
        body: JSON.stringify({ title, url, id: currentId})
    })

    titleInputEl.value = '';
    URLInputEl.value = '';

    editBtnEl.disabled = true;
    addBtnEl.disabled = false;

    await handleLoadBtn();
}