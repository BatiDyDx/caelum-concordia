var link = document.getElementsByName('secret-link')[0];
link.addEventListener('copy', function(){
    window.location.href = '/admin';
})