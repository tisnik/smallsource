$(document).ready(function(){
        interval = setInterval(function () {

            req = $.ajax({
                type: 'POST',
                url: "/app/upload_success/update"
            });

            req.done(function (data) {
                if (data == 'END') {
                  $(clearInterval(interval))
                } else {
                  $('.my_data').html(data);
                }

            })
        }, 1000)

});
