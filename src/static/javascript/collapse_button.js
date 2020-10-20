var buttons = document.getElementsByName('btn-collapse-category');
var card_body = document.getElementsByName('category-card-body');
collapseCondition = false
for (let i = 0; i < buttons.length; i++){
    buttons[i].addEventListener('click', function(){
        collapseCondition = !collapseCondition;
        if(collapseCondition==false){
            buttons[i].style.rotate = '180deg';
            card_body[i].style.display = 'Block'
        }else{
            buttons[i].style.rotate = '0deg';
            card_body[i].style.display = 'None'
        }
    })
}