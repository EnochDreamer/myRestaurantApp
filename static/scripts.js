const menu=document.querySelector('#menu')
const overlay=document.getElementById('overlay')
const link_wrapper=document.querySelector('.link-wrapper')
const form=document.getElementById('form')
const searchkey=document.getElementById('searchkey').value
const item=document.querySelector('.item')


form.onsubmit = function(e){
    console.log(e);
    fetch('/restaurants/search/',{
      headers:{
         'content-Type':'application/json'
      }
    })
    .then(function(response){
        return response.json();
     })
     .then(function(jsonResponse){
        console.log(jsonResponse);
        const liItem=document.createElement('LI');
        liItem.innerHTML=jsonResponse['description'];
        document.getElementById('todos').appendChild(liItem);
        document.getElementById('error').className='hidden';
    
     })
}

item.onclick= function(e){
    console.log(e);
}

let openmenu=false


function openingMenu(){
    openmenu=true
    link_wrapper.style.width='200px'
    overlay.style.display='block'
}

function closingMenu(){
    openmenu=false
    link_wrapper.style.width='0px'
    overlay.style.display='none'
}

menu.addEventListener('click', function(){
    if (!openmenu) {
        openingMenu()
    }
})


overlay.addEventListener('click', function(e){
    console.log(e)
    if (openmenu) {
        closingMenu()
    }
})

