$(document).ready(function() {
    $('#myTable').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

$(document).ready(function() {
    $('#myTable2').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

$(document).ready(function() {
    $('#myTable3').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

$(document).ready(function() {
    $('#myTable4').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

var getCookie = function (name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };

$(document).ready(function() {
  $('#myTable .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.ajax({
        url: "http://127.0.0.1:8000/pdc/projets/delete/"+id,
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response){
            $this.parent().fadeOut(800);
        }
    });
  });

  $('#myTable2 .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.ajax({
        url: "http://127.0.0.1:8000/pdc/clients/delete/"+id,
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response){
            $this.parent().fadeOut(800);
        }
    });
  });

  $('#myTable3 .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.ajax({
        url: "http://127.0.0.1:8000/pdc/collaborateurs/delete/"+id,
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response){
            $this.parent().fadeOut(800);
        }
    });
  });

  $('#myTable4 .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.ajax({
        url: "http://127.0.0.1:8000/pdc/collaborateurs/delete/"+id,
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function(response){
            $this.parent().fadeOut(800);
        }
    });
  });
});
