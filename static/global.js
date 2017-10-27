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

    $('#turnOffAlarm').click(function() {

        data = {
            go: 'off'
        }

        $.ajax({
            type: "POST",
            url: "/alarm",
            data: data,
            success: function(data) {
                location.reload();
            }
        })
    });

    $('#turnOnAlarm').click(function() {

        data = {
            go: 'on'
        }

        $.ajax({
            type: "POST",
            url: "/alarm",
            data: data,
            success: function(data) {
                location.reload();
            }
        })
    });

    $('#startAlarm').click(function() {
        data = {
            client_id: $(this).attr('data-id'),
            status: 'on'
        }
        $.ajax({
            type: "POST",
            url: "/alarm/client",
            data: data,
            success: function(data) {
            }
        })
    });

    $('#stopAlarm').click(function() {
        data = {
            client_id: $(this).attr('data-id'),
            status: 'off'
        }
        $.ajax({
            type: "POST",
            url: "/alarm/client",
            data: data,
            success: function(data) {
            }
        })
    });

});