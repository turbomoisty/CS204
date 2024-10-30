const user_option = document.getElementsByClassName('option_help')

for (let i = 0; i < user_option.length; i++){
    user_option[i].addEventListener('mouseover', function(){
        if (user_option[i]){
            user_option[i].textContent = 'Changed!';
            console.log('Hovered over')
        }
    });

    user_option[i].addEventListener('mouseout', function(){
        if (user_option[i]){
            user_option[i].textContent = '?';
            console.log('Unhovered')

        }
    });
}