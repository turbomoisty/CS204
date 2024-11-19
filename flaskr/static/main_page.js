const menu = document.getElementById('menu');
const icon_items = document.querySelectorAll('.icon_item');
const text_box = document.querySelectorAll('#text_box_display');

Array.from(document.getElementsByClassName('menu-item')).forEach((item, index) => {
        item.onmouseover =() =>{
            menu.dataset.activeIndex = index;
        };
    });



