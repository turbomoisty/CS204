const menu = document.getElementById('menu');
const icon_items = document.getElementsByClassName('icon-item');
const text_box = document.querySelectorAll('#picture-list > #text_box_display');


//Array for the left text to ensure scrolling works as intended
Array.from(document.getElementsByClassName('menu-item')).forEach((item, index) => {
        item.onmouseover =() =>{
            menu.dataset.activeIndex = index;
        };
    });

    text_box.forEach(t_box =>{ // Makes sure all boxes are hidden by default.
        t_box.style.display = 'none';
    });

for (let i =0; i < icon_items.length; i++){
    icon_items[i].addEventListener('mouseover', ()=>{
        text_box.forEach(t_box =>{
            t_box.style.display = 'none';
        });

        setTimeout(function(){
            if (text_box[i]) {
                text_box[i].style.animation = 'pop-up 333ms ease-in-out forwards';
                text_box[i].style.display = 'block';
            }
        },100)

    });

    // This whole portion is sort of janky, but it works.
    if (text_box[i]){
        icon_items[i].addEventListener('mouseleave', () => {
            text_box[i].style.animation = 'pop-up 233ms ease-in-out reverse';
            text_box[i].style.display = 'none';
        });
    };
}

