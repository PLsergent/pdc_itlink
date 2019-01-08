$(document).ready(function() {
    $('#myTable').DataTable({
      orderFixed: [[ 4, "asc" ], [7, "asc"]],
      paging:         false,
    });

// ====== Notification =======
$(document).on('click', '.undo', function() {
    $("#undo").addClass('is-hidden');
    return false;
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

// Delete button
    $('.mydelete').on('click', function(){
      var $this = $(this)
      var id = $(this).data('id');
      $.confirm({
        title: 'Delete pop-up',
        content: 'The deletion of a command may delete one or multiple\
                  objects of affectation view. Do you want to proceed anyway?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: "http://127.0.0.1:8000/pdc/commandes/delete/"+id,
                  type: 'POST',
                  beforeSend: function(xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                  },
                  success: function(response){
                      $this.closest('tr').fadeOut(250);
                      $("#undo").fadeIn().removeClass("is-hidden");
                      $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_command/Commande/"+id);
                      setTimeout(function() {
                          $('#undo').addClass("is-hidden");
                      }, 6000);
                  },
                  error: function(xhr, text, code){
                    if(text == 'error' && code == 'Forbidden'){
                      $('.modal').addClass("is-active");
                      $(document).on('click', '.modal-background', function(){
                          $('.modal').removeClass("is-active");
                      });
                      $(document).on('click', '#modaldelete', function(){
                          $('.modal').removeClass("is-active");
                      });
                    }
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
