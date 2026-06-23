document.querySelectorAll(

'.dropdown-btn'

)

.forEach(button=>{


button.addEventListener(

'click',()=>{


const submenu=button.nextElementSibling;


submenu.classList.toggle(

'active'

);


});

});

themeBtn.onclick=()=>{


document.body.classList.toggle(

'dark'

);


}
menuBtn.onclick=()=>{


sidebar.classList.toggle(

'-translate-x-full'

);


}