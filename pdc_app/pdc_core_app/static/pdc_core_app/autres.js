$(document).ready( function () {
    $('#myTable').DataTable({
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 4
      }
    }
    );
    var table = new $.fn.dataTable.Api( '#myTable' );

// Color cells
    table.cells().every( function () {
        if ( this.data() > 100 ){
          $(this.node()).addClass( 'has-background-danger' );
        }
        else if ( this.data() >= 80 ) {
            $(this.node()).addClass( 'has-background-success' );
        }
        else if ( this.data() < 80 &&  this.data() >= 50 ) {
            $(this.node()).addClass( 'has-background-primary' );
        }
        else if ( this.data() < 50 && this.data() != 0) {
            $(this.node()).addClass( 'has-background-warning' );
        }
        else {
            $(this.node()).removeClass( 'has-background-success' );
        }
    });

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
      var $this = $(this);
      var id = $(this).data('id');
      var row = table.cell($(this)).index().row;
      var idRow = table.rows().eq(0).indexOf(row);
      $.confirm({
        title: 'Deletion pop-up',
        content: 'Do you want to proceed ?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: "http://127.0.0.1:8000/pdc/autres/assign/delete/"+id,
                  type: 'POST',
                  beforeSend: function(xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                  },
                  success: function(response){
                      $this.closest('tr').fadeOut(250);
                      $("#myTable > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#undo").fadeIn().removeClass("is-hidden");
                      $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_autres/RepartitionActivite/"+id);
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
