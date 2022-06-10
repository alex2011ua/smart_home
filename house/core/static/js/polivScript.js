let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
let data = {};
dvor.addEventListener('click', function(event) {
    if (event.target.classList.contains('DHUM') | event.target.classList.contains('DHUM2') ) {
        data = {'off': event.target.dataset.on};
        console.log(data);
         $.ajax({
        url: '',
        method: 'POST',
        data: data,
        success: function (text) {
            event.target.remove()
        },
        error: function (text) {
            alert('error');
        },
    })
    }
    if (event.target.classList.contains('need')) {
        data = {'on': event.target.dataset.on};
         $.ajax({
        url: '',
        method: 'POST',
        data: data,
        success: function (text) {
            let img = document.querySelector('.no-display');
            let clon = img.cloneNode(true);
            clon.dataset.on = event.target.dataset.on;
            clon.classList.remove('no-display');
            event.target.before(clon);
        },
        error: function (text) {
            alert('error');
        },
    })
    }
    if (event.target.dataset.hasOwnProperty('on')) {
        data = {'on': event.target.dataset.on};
    }
    if (event.target.dataset.hasOwnProperty('off')) {
        data = {'off': event.target.dataset.off};
    }
    }, true
);

