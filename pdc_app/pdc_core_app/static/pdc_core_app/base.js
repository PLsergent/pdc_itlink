$(document).on('click', '#notif', function() {
    $(this).addClass('is-hidden');
    return false;
});

setTimeout(function() {
    $('#notif').fadeOut('slow');
}, 4000);
