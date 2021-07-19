console.log('start script')

let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });

let words_obj=0;
 $.ajax({
    url: '',
    method: 'POST',
    data: 'data',
     async: false,
    success: function (text) {
        console.log('__ok__');

    words_obj = text;
    },
    error: function (text) {
        console.log('__error__');
        console.log(text);
        alert('error');
    },
});

console.log(words_obj);
let words_list = Object.keys(words_obj);
let ind = Math.floor(Math.random() * words_list.length);

console.log(words_obj[words_list[ind]], words_list[ind]);

document.getElementById("word").innerHTML = words_list[ind];
function start(){
    console.log('submit');
    let ind = Math.floor(Math.random() * words_list.length);

console.log(words_obj[words_list[ind]], words_list[ind]);

document.getElementById("word").innerHTML = words_list[ind];
}
