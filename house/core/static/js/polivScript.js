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
    if (event.target.dataset.hasOwnProperty('on')) {
        data = {'on': event.target.dataset.on};
        console.log("hasOwnProperty(\'on\')");
    };
    if (event.target.dataset.hasOwnProperty('off')) {
        data = {'off': event.target.dataset.off};
        console.log("hasOwnProperty(\'off\')");
    };


    $.ajax({
        url: '',
        method: 'POST',
        data: data,
        success: function (text) {
            console.log('__ok__');
            console.log(text);
            alert('success');
        },
        error: function (text) {
            console.log('__error__');
            console.log(text);
            alert('error');
        },
    })

    }, true);

