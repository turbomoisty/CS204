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
        const selectedDiv_r = document.querySelector(`.${selectedValue_r}`);

        if (selectedDiv_r) {
            selectedDiv_r.style.display = 'flex';
        }
    }
});


async function generateHash(whatever_side){
    const userTextInput = document.getElementById(`text_input_${whatever_side}`).value;
    const hashType = document.getElementById('hash_value_type').value;
    const result_answer = document.getElementById('compare_result');


    if(!userTextInput){
        result_answer.innerText = 'Enter a value first!';
        return;// Not working??? I don't know why
    }

    const response = await fetch('/gen_hash', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            data: userTextInput,
            hash_type: hashType
        })
    });

    const result = await response.json();
    if(response.ok){
        document.getElementById(`hash_output_${whatever_side}`).value = result.hash;
        result_answer.innerText =''
    }else{
            alert(result.error);
        }
}

async function compareHash(){
    const hash_l = document.getElementById('hash_output_l').value;
    const hash_r = document.getElementById('hash_output_r').value;

    const response = await fetch('/check_hash',{
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify({
            hash_l: hash_l,
            hash_r: hash_r
        })

    });

    const result = await response.json();
    const compareText = result.match ? 'Hashes Match!' : 'Hashes do not match';

    const result_answer = document.getElementById('compare_result');

    result_answer.innerText = compareText;
    if (compareText === 'Hashes Match!'){
        result_answer.style.color = '#9aff79';
    } else {
        result_answer.style.color = 'red';
    }
}