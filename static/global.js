$(document).ready(function() {

    $('#clientAdd').submit(function(e) {

        e.preventDefault()

        $('div[data-step="1"]').hide();

        $.ajax({
            type: "POST",
            url: "/client/add",
            data: $('#clientAdd').serialize(),
            success: function(data) {
                $('div[data-step="2"] h1').text(data['client_id']);
                $('div[data-step="2"] span').text(data['name']);
                $('div[data-step="2"]').show();
            }
        })

    })

});