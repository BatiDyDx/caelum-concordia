var img = document.getElementById('URL_img');
var refresh_button = document.getElementById('refresh_button');
var url = document.getElementById('URL');

if(img.getAttribute('src') == ''){
    img.style.display = 'none'
}

refresh_button.addEventListener('click', function(){
    img.src = url.value;
    img.style.display = 'initial';
})