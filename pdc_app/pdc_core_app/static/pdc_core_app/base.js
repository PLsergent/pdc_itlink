$(document).on('click', '.notification', function() {
    $(this).addClass('is-hidden');
    return false;
});

setTimeout(function() {
    $('#notif').fadeOut('fast');
}, 3000);
