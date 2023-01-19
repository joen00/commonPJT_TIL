
// ajax
var sendBtn = document.querySelector('#send');
sendBtn.addEventListener("click", sendAjax);
function sendAjax(event){
    var canvas = document.querySelector('canvas');
    
    $.ajax({
        // ### code 작성 ###
        url: 'http://localhost:5000/pp',
        method: 'GET',
    }).done((result) => {
        var ans = document.querySelector('#answer')
        ans.innerHTML = result['answer']
    }).fail((error) => {
        console.error(error)
    })
}