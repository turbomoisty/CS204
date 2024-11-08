const user_help = document.getElementsByClassName('option_help') /* small '?' at corner */
const tool_tip = document.getElementsByClassName('tool_tip_text') /* Display help box.  */

for (let i = 0; i < user_help.length; i++){
    user_help[i].addEventListener('mouseover', function(){
        if(i === 0){
            if (user_help[i]){
                tool_tip[0].style.display = 'block';
            }

        tool_tip[i].addEventListener('mouseenter', function(){
                tool_tip[i].style.display = 'block';
            })


        tool_tip[i].addEventListener('mouseleave', function(){
            tool_tip[i].style.display = 'none';
        })
        }  /*  -----------------END OF FIRST i ELEMENT-------------------- */
        else if(i=== 1){
            if (user_help[i]){
                tool_tip[1].style.display = 'block';
            }

            tool_tip[i].addEventListener('mouseenter',function(){
                tool_tip[i].style.display = 'block';
            })

            tool_tip[i].addEventListener('mouseleave', function(){
                tool_tip[i].style.display = 'none';
            })
        }  /*  -----------------END OF SECOND i ELEMENT-------------------- */

        else if(i===2){
            if (user_help[i]){
                tool_tip[i].style.display = 'block'
            }

            tool_tip[i].addEventListener('mouseover', () =>{
                tool_tip[i].style.display = 'block';
            }, false)

            tool_tip[i].addEventListener('mouseleave', () =>{
                tool_tip[i].style.display = 'none';
            }, false) 
        }   /*  -----------------END OF THIRD i ELEMENT-------------------- */

        else if(i===3){
            if(user_help[i]){
                tool_tip[i].style.display ='block';
            }

            tool_tip[i].addEventListener('mousover', ()=>{
                tool_tip[i].style.display = 'block';
            }, false)

            tool_tip[i].addEventListener('mouserleave', ()=>{
                tool_tip.style.display='none';
            }, false)
        }

    }); 


}