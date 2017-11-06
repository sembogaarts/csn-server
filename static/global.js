$(document).ready(function() {

    $('#clientAdd').submit(function(e) {
        // Disable default event
        e.preventDefault();
        // Hide the form
        $('div[data-step="1"]').hide();
        // Perform a post request and show the result
        $.ajax({
            type: "POST",
            url: "/client/add",
            data: $('#clientAdd').serialize(),
            success: function(data) {
                $('div[data-step="2"] h1').text(data['client_id']);
                $('div[data-step="2"] span').text(data['name']);
                $('div[data-step="2"]').show();
            }
        });
    })

    $('#turnOffAlarm').click(function() {
        toggleServerAlarm({turn:'off'});
    });

    $('#turnOnAlarm').click(function() {
        toggleServerAlarm({turn:'on'});
    });

    function toggleServerAlarm(data) {
        $.ajax({
            type: "POST",
            url: "/alarm",
            data: data,
            success: function() {
                location.reload();
            }
        });
    }

    $('#startAlarm').click(function() {
        data = {
            client_id: $(this).attr('data-id'),
            status: 1
        };
        toggleClientAlarm(data);
    });

    $('#stopAlarm').click(function() {
        data = {
            client_id: $(this).attr('data-id'),
            status: 0
        };
        toggleClientAlarm(data);
    });

    $('#triggerAlarm').click(function() {
        data = {
            client_id: $(this).attr('data-id'),
            status: 3
        };
        toggleClientAlarm(data);
    });

    function toggleClientAlarm(data) {
        $.ajax({
            type: "POST",
            url: "/alarm/client",
            data: data,
            success: function() {
                // Choose a word depending on status
                switch(data.status) {
                    case 0:
                        status = 'uitgezet';
                        break;
                    case 1:
                        status = 'aangezet';
                        break;
                    case 3:
                        status = 'aangezet, en geactiveerd'
                }
                // Give feedback to the user
                swal(
                  'Success!',
                  'Het alarmsysteem is op de client ' + status +  '.',
                  'success'
                );
            }
        });
    }

});