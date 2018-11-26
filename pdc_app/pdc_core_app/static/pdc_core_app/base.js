$(document).on('click', '.notification > button.delete', function() {
    $(this).parent().addClass('is-hidden');
    return false;
});

setTimeout(function() {
    $('#notif').fadeOut('fast');
}, 3000);
