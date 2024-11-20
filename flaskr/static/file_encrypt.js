const drop_area = document.getElementById('drop_area');
const input_file = document.getElementById('input_file');
const file_view = document.getElementById('file_view');
const pass_form = document.getElementById('option_button');

const toggle_p_visibility = document.querySelector('#togglePassword')
const password_form = document.querySelector('#passcode_input')

pass_form.style.display = 'none'; 

input_file.addEventListener('change',uploadFile);

function uploadFile(){
        const file = input_file.files[0];

        if(file){

            pass_form.style.display = 'grid'; 

            let link = URL.createObjectURL(file);
    
            file_view.style.backgroundImage = `url(${link})`;
            file_view.querySelector('p').textContent = file.name;
            alert(`--${file.name}-- has been sucessfully uploaded`)
            file_view.querySelector('img').style.display = '';


            drop_area.addEventListener('dragover', (e)=>{
                e.preventDefault();
            
            });
            
            drop_area.addEventListener('drop', (e)=>{
                e.preventDefault();
                input_file.files = e.dataTransfer.files;
                uploadFile();

            });
        } else{
            alert('Somthing went wrong!')
        }

        toggle_p_visibility.addEventListener('click', function(){

            const type = password_form.getAttribute("type") === "password" ? "text" : "password";
            password_form.setAttribute("type", type);
            
            // icon togglking
            this.classList.toggle("bi-eye");
            this.classList.toggle("bi-eye-slash")
        });

    };

    /*Errror mesage Function*/
    const error_box = document.getElementById('error-box')
    function displayError(){
        error_box.style.display='none';
    }

