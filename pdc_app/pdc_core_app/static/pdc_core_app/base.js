$(document).on('click', '#notif', function() {
    $(this).addClass('is-hidden');
    return false;
});

$(document).on('click', '.delete', function() {
    $("#notif").addClass('is-hidden');
    return false;
});


setTimeout(function() {
    $('#notif').fadeOut('slow');
}, 4000);
