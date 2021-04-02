let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
dvor.addEventListener('click', function(event) {
    let data = {};
    if (event.target.dataset.hasOwnProperty('on')) {
        data = {'on': event.target.dataset.on};
    }
    alert('SAD');

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
            console.log('__1__');
            console.log(text);
            alert('error');
        },
    })

    }, true);
