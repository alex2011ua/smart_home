let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
dvor.addEventListener('click', function(event) {
    console.log('Dvor');
    console.log(event.target);
    let data = {};
    if (event.target.classList.contains('DHUM')) {
        data = {'off': event.target.dataset.on};
        console.log(data);
         $.ajax({
        url: '',
        method: 'POST',
        data: data,
        success: function (text) {
            console.log('__ok__');
            console.log(text);
            event.target.remove()
        },
        error: function (text) {
            console.log('__error__');
            console.log(text);
            alert('error');
        },
    })
    }
    if (event.target.classList.contains('need')) {
        data = {'on': event.target.dataset.on};
        console.log(data);
         $.ajax({
        url: '',
        method: 'POST',
        data: data,
        success: function (text) {
            console.log('__ok__');
            console.log(text);
            let img = document.querySelector('.no-display');
            let clon = img.cloneNode(true);
            clon.dataset.on = event.target.dataset.on;
            clon.classList.remove('no-display');
            event.target.before(clon);
        },
        error: function (text) {
            console.log('__error__');
            console.log(text);
            alert('error');
        },
    })
    }



    if (event.target.dataset.hasOwnProperty('on')) {
        data = {'on': event.target.dataset.on};
        console.log("hasOwnProperty(\'on\')");
    };
    if (event.target.dataset.hasOwnProperty('off')) {
        data = {'off': event.target.dataset.off};
        console.log("hasOwnProperty(\'off\')");
    };




    }, true);

