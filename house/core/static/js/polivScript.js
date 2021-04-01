let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
$.ajaxSetup({
        headers: {
            'X-CSRFToken': csrftoken
        }
    });
sad.addEventListener('click', function(event) {
    if (event.target.dataset.hasOwnProperty('on')){
        if (event.target.dataset.on ==='sad'){
            alert('dataset.on')
        }}
    alert('SAD');
    let data = {123:'gvh'};
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
