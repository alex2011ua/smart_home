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
        alert('"Не получен список слов с сервера"');
    },
});
console.log(words_obj)




//
// let control_state = words_obj['control_state'];
// delete words_obj['control_state'];
// let words_list = Object.keys(words_obj);



var gerund = document.getElementById('gerund_button'); // кнопка для выученого слова
var infinitiv = document.getElementById('infinitive_button'); // кнопка для сложного слова
var all_of_them = document.getElementById("all_of_them");    // счетчик слов

var count_words = document.getElementById("count_is");    // счетчик слов




let answer = document.getElementById("result");             // правильный ответ
document.getElementById("word").innerHTML = word.english;
let ok =  document.getElementById("ok");
let err = document.getElementById("error");

var uptate_scrieen = function(){
    ind = Math.floor(Math.random() * words_obj.length);
     word = words_obj[ind];

     document.getElementById("word").innerHTML = word.word;
     count_words.innerHTML = words_obj.length;
}
uptate_scrieen();

function start(button_pressed){
     let inp = button_pressed;

     if (inp.toLowerCase() === word.answer){
         console.log('верно - удаляю');
         answer.innerText = " - " + word;
         delete words_obj[word];
         ok.style.display = 'none';
         err.style.display = 'block';
         answer.style.display = 'block';
     }

    else{

         answer.style.display = 'block'
         answer.innerText = " - " + word;
         ok.style.display = 'block'
         ok.innerText = inp + " - не верно.";
         err.style.display = 'none';
     }

     uptate_scrieen();
}

gerund.onclick = function(){
     start('gerund');
};
infinitiv.onclick = function(){
     start('infinitive');
};
all_of_them.onclick = function(){
     start('all');
};

