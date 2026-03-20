  const checkBoxAllEl = document.getElementById('select-all')

    checkBoxAllEl.addEventListener('change', handleCheckBox)

    function handleCheckBox(){
        const checkBoxSingleEl = document.querySelectorAll('input[name="selected_tags"]')

        checkBoxSingleEl.forEach(el => {
            el.checked = this.checked;
        })
    }