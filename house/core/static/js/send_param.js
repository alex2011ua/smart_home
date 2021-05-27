
var send_param_bot = function(){
            $.ajax({
                url: 'test/string_arduino_to_bot/',
                data: 'data',
                method: 'GET',
                dataType: 'json',
                success: function(data){
                    console.log(data);
                }
            });}