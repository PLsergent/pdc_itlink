$(document).ready(function() {
    $('#myTable').DataTable({
      paging:         false,
    });

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

    $('.mydelete').on('click', function(){
      var $this = $(this)
      var id = $(this).data('id');
      var row = $(this).closest('td').data('dt-row')
      $.confirm({
        title: 'Confirm pop-up',
        content: 'Do you want to proceed ?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: "http://127.0.0.1:8000/pdc/commandes/delete/"+id,
                  type: 'POST',
                  beforeSend: function(xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                  },
                  success: function(response){
                      $this.closest('tr').fadeOut(500);
                      $("#myTable tr").slice(row+1,row+2).fadeOut(500);
                  }
              });
            },
            cancel: function () {
                return;
            }
        }
      });
    });
});
