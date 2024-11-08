const hash_option_drop_down = document.getElementById('hash_l');
const option_div = document.querySelectorAll('.option_l');

for (let i = 1; i < option_div.length; i ++){
    option_div[i].style.display = 'none';
}

hash_option_drop_down.addEventListener('change', () =>{
    let selectedValue = hash_option_drop_down.value;

    for (let i = 0; i < option_div.length; i ++){
        option_div[i].style.display = 'none';
    }


    if (selectedValue) {
        const selectedDiv = document.querySelector(`.${selectedValue}`);
        if (selectedDiv) {
            selectedDiv.style.display = 'flex';
        }
    }

});


const hash_option_drop_down_r = document.getElementById('hash_r');
const option_div_r = document.querySelectorAll('.option_r');

for (let i = 1; i < option_div_r.length; i ++){
    option_div_r[i].style.display = 'none';
}

hash_option_drop_down_r.addEventListener('change', () =>{
    let selectedValue_r = hash_option_drop_down_r.value;

    for (let i = 0; i < option_div_r.length; i ++){
        option_div_r[i].style.display = 'none';
    }

    if (selectedValue_r) {
        const selectedDiv_r = document.querySelector(`.${selectedValue_r}`); //Remember that the selectedValue_r is a CLASS selector, took me 2 hours to wonder why the Event listener wasn't working

        if (selectedDiv_r) {
            selectedDiv_r.style.display = 'flex';
        }
    }

})