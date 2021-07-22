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

let words_list = Object.keys(words_obj);
let ind = Math.floor(Math.random() * words_list.length);
var dellete_word_button = document.getElementById('dellete_word'); // кнопка для удаления слова
var learned = document.getElementById('learned'); // кнопка для выученого слова
var heavy = document.getElementById('heavy'); // кнопка для сложного слова
var count_words = document.getElementById("count_is");                 // счетчик слов
count_words.innerHTML = words_list.length;
console.log(words_obj[words_list[ind]], words_list[ind]);
let answer = document.getElementById("result");             // правильный ответ
document.getElementById("word").innerHTML = words_list[ind];

function start(){
    let inp = document.getElementById("exampleFormControlInput1").value.trim();
    if (inp.toLowerCase() == words_obj[words_list[ind]].toLowerCase()){
        console.log('верно - удаляю');
        answer.innerText = words_obj[words_list[ind]] + " - " + words_list[ind];
        delete words_obj[words_list[ind]];
        words_list = Object.keys(words_obj);
        document.getElementById("exampleFormControlInput1").value = '';

        let ok =  document.getElementById("ok");
        ok.style.display = 'none';
        let err = document.getElementById("error");
        err.style.display = 'block';
        dellete_word_button.style.display = 'none';
        answer.style.display = 'block'

    }
    else{
        document.getElementById("exampleFormControlInput1").value = '';
        console.log("не верно");
        answer.style.display = 'block'
        answer.innerText = words_obj[words_list[ind]] + " - " + words_list[ind];
        let ok =  document.getElementById("ok");
        ok.style.display = 'block'
        ok.innerText = "не верно: "+  inp;
        let err = document.getElementById("error");
        err.style.display = 'none';

        dellete_word_button.style.display = 'block';
        let to_del = ind;
        heavy.onclick = function () {
            console.log(words_list[to_del]);
            $.ajax({
                url: 'heavy',
                method: 'POST',
                data: words_list[to_del],
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
        }
        dellete_word_button.onclick = function() {
            delete words_obj[words_list[to_del]];
            words_list = Object.keys(words_obj);
            console.log('Хоть и не верно  - удаляю');
            dellete_word_button.style.display = 'none'

        }
    //do processing

    }
        learned.onclick = function () {
                console.log(words_list[ind]);
             $.ajax({
                url: 'learned',
                method: 'POST',
                data: words_list[ind],
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

        }
    ind = Math.floor(Math.random() * words_list.length);
    console.log(words_obj[words_list[ind]], words_list[ind]);
    document.getElementById("word").innerHTML = words_list[ind];
    count_words.innerHTML = words_list.length;
}
