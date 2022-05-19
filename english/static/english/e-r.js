let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
    headers: {
        'X-CSRFToken': csrftoken
    }
});

let words_obj = 0;
$.ajax({
    url: '/english/api/r_e_words',
    method: 'GET',

    async: false,
    success: function (text) {
        console.log('__ok__');
        words_obj = text;
    },
    error: function (text) {
        console.log('__error__');
        console.log(text);
        alert('"Не получен "');
    },
});
console.log("print obj:")
console.log(words_obj);
/*
Array(20) [ {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, {…}, … ]
0: Object { id: 16, english: "bride", russian: "невеста", … }

control: false
english: "bride"
heavy: false
id: 16
info: ""
irregular_verbs: false
learned: false
lesson: 1
phrasal_verbs: false
repeat_in_progress: true
repeat_learn: 3
russian: "невеста"

1: Object { id: 52, english: "paint", russian: "краска", … }
2: Object { id: 68, english: "stomachache", russian: "боль в животе", … }
3: Object { id: 83, english: "to bake", russian: "печь", … }
4: Object { id: 89, english: "camera", russian: "фотаппарат", … }
*/

let random_word = words_obj[Math.floor(Math.random() * words_obj.length)];

var dellete_word_button = document.getElementById('dellete_word'); // кнопка для удаления слова

var count_words = document.getElementById("count_is");    // счетчик слов
var submit_button = document.getElementById("submit_button");    // счетчик слов
var vvod = document.getElementById("vvod");    // счетчик слов
var learned = document.getElementById('learned'); // кнопка для выученого слова
var heavy = document.getElementById('heavy'); // кнопка для сложного слова
var not_heavy = document.getElementById('not_heavy'); // кнопка для сложного слова
count_words.innerHTML = words_obj.length;
var word_index_to_dell = false;
let answer = document.getElementById("result");             // правильный ответ
document.getElementById("word").innerHTML = random_word.russian;
let ok = document.getElementById("ok");
let err = document.getElementById("error");

function start() {
    let inp = document.getElementById("vvod").value.trim();
    let to_del = random_word;
    if (inp.toLowerCase() === random_word.english.toLowerCase()) {
        answer.innerText = random_word.english + " - " + random_word.russian;
        dell_word();

        let word_index = words_obj.indexOf(random_word);
        if (word_index !== -1) {
            words_obj.splice(word_index, 1);
        }

        document.getElementById("vvod").value = '';
        ok.style.display = 'none';
        err.style.display = 'block';
        dellete_word_button.style.display = 'none';
        answer.style.display = 'block';

    } else {
        $.ajax({
            url: '/english/api/word/' + random_word.id + "/",
            method: 'PATCH',
            data: {'repeat_learn': random_word.repeat_learn + 1},
            success: function (text) {
                console.log(text);
                console.log(random_word.repeat_learn);
            },
            error: function (text) {
                console.log(text);
                alert(text);
            },
        });

        document.getElementById("vvod").value = '';
        console.log("не верно");
        answer.style.display = 'block'
        answer.innerText = random_word.english + " - " + random_word.russian + "(" + random_word.id + ")";
        ok.style.display = 'block'
        ok.innerText = inp + " - не верно.";
        err.style.display = 'none';
        dellete_word_button.style.display = 'inline';
    }

    dellete_word_button.onclick = function () {
        dell_word(1);
    }
    heavy.onclick = function () {
        console.log(to_del);
        $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: {'heavy': true},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });
    }
    not_heavy.onclick = function () {
        console.log(to_del);
        $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: {'heavy': false},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });
    }
    learned.onclick = function () {
        console.log(to_del);
        $.ajax({
            url: '/english/api/word/' + to_del.id + "/",
            method: 'PATCH',
            data: {'learned': true},
            success: function (text) {
                console.log('__ok__');
            },
            error: function (text) {
                console.log('__error__');
                console.log(text);
                alert('error');
            },
        });
    }
    word_index_to_dell = words_obj.indexOf(to_del);
    if (word_index_to_dell !== -1) {
        words_obj.splice(word_index_to_dell, 1);
    }
    console.log('Хоть и не верно  - удаляю');
    dellete_word_button.style.display = 'none';
    count_words.innerHTML = words_obj.length;
    console.log('words_obj.length-', words_obj.length)


    random_word = words_obj[Math.floor(Math.random() * words_obj.length)];
    if (random_word == undefined) {
        alert("Слова закончились, отдохни!!!");
    }
    document.getElementById("word").innerHTML = random_word.russian;
    count_words.innerHTML = words_obj.length;
    function dell_word(nnn = 0){
        if (random_word.repeat_learn >= 1) {
            $.ajax({
                url: '/english/api/word/' + to_del.id + "/",
                method: 'PATCH',
                data: {'repeat_learn': to_del.repeat_learn - 1 - nnn},
                success: function (text) {
                    console.log(text)
                },
                error: function (text) {
                    console.log(text);
                    alert(text);
                },
            });
        } else {
            $.ajax({
                url: '/english/api/word/' + to_del.id + "/",
                method: 'PATCH',
                data: {'learned': true},
                success: function (text) {
                    console.log(text)
                },
                error: function (text) {
                    console.log(text);
                    alert(text);
                },
            });
        }
    }
}

submit_button.onclick = function () {
    start();
};
vvod.onsubmit = function () {
    start();
};

// Make sure this code gets executed after the DOM is loaded.
document.querySelector("#vvod").addEventListener("keyup", event => {
    if (event.key !== "Enter") return; // Use `.key` instead.
    document.querySelector("#submit_button").click(); // Things you want to do.
    event.preventDefault(); // No need to `return false;`.
});

