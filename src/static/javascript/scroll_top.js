var scrollButton = document.getElementById('scroll_button');

var scrollTop = function() {
    window.scrollTo(0, 0);
};

scrollButton.addEventListener('click', function(){
    scrollTop();
})