const drop_area = document.getElementById('drop_area');
const input_file = document.getElementById('input_file');
const file_view = document.getElementById('file_view');
const pass_form = document.getElementById('option_button');

input_file.addEventListener('change',uploadFile);

function uploadFile(){
        const file = input_file.files[0];

        if(file){
    
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
                pass_form.style.display = 'grid'; 
        } else{
            alert('Somthing went wrong!')
        }
    };
    