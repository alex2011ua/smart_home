'use strict';

(function (){
function focus(event){
    if (event.target.tagName === 'INPUT'){
        let inp = event.target;
        if (inp.classList.contains(params.inputErrorClass)){
        }
    }
};

function valid(value, input){
    if (input.dataset.hasOwnProperty('required')){
        if (!value){return "нет значения";}
    }
    if (input.dataset.hasOwnProperty('validator')){
        if (!value){return null;}
        if (input.dataset.validator =='letters'){
            let m = (value.match(/^[a-zA-Zа-яА-Я]*/));
            if (m[0] !== m.input){
                return "Нужно вводить только буквы";
            }
        }
        if (input.dataset.validator =='regexp'){
            let reg = input.dataset.validatorPattern;
            reg = new RegExp(reg);
            let p = reg.test(value)
            if (!p){
                return "Нужно вводить только шаблон";
            }
        }

        if (input.dataset.validator =='number'){
            let m = (value.match(/^[0-9]*/));
            if (m[0] !== m.input){
                return "Нужно вводить только цыфры";
            }
            if (input.dataset.hasOwnProperty('validatorMin')){
                let min = input.dataset.validatorMin;
                if (parseInt(value) < parseInt(min)){
                    return "min";
                }
            }
            if (input.dataset.hasOwnProperty('validatorMax')){
                let max = input.dataset.validatorMax;
                if (parseInt(value) > parseInt(max)){
                    return 'max'
                }
            }
        }
    }
    return NaN;
};
window.validateForm = function (params) {
    let form = document.getElementById(params.formId);
    form.addEventListener('submit', function (event) {
        event.preventDefault();
        form.classList.remove(params.formValidClass);
        form.classList.remove(params.formInvalidClass);
        var inputs = Array.from(
            document.querySelectorAll('#' + params.formId + ' input')
        );
        var hasError = false;
        for (var i = 0; i < inputs.length; i++) {
            var input = inputs[i];
            let value = input.value;
            if (valid(value, input)) {
                input.classList.add(params.inputErrorClass);
                hasError = true;
            }
        }
        if (hasError){
            form.classList.add(params.formInvalidClass);
    }else{
        form.classList.add(params.formValidClass);
    }
    });

    form.addEventListener("focusin", function (event){
        if (event.target.tagName === 'INPUT'){
            let inp = event.target;
            if (inp.classList.contains(params.inputErrorClass)){
                inp.classList.remove(params.inputErrorClass);
            }
        }
    });
    form.addEventListener("focusout", function(event){
        if (event.target.tagName === 'INPUT'){
            let value = event.target.value;
            let inp = event.target;
            let error = valid(value, inp);
            if (error){
                inp.classList.add(params.inputErrorClass);
            }

        }
    });
}
}());
