$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      sScrollX:     "100%",
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 9
      },
    }
    );
    var table = new $.fn.dataTable.Api( '#myTable' );

    table.cells().every( function () {
        var data = this.data()
        if (data % 1 === 0){
          if ( this.data() >= 80 ) {
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
        }
    } );

    $('#switchAll').prop('checked', true);
    $('#switchE').prop('checked', false);
    $('#switchP').prop('checked', false);

    $('#switchE').on('change', function filter(){
      tableP.fnFilter('True', 8);
      $('#switchP').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
    $('#switchP').on('change', function filter(){
      tableP.fnFilter('False', 8);
      $('#switchE').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
    $('#switchAll').on('change', function filter(){
      tableP.fnFilter('True|False', 8, true);
      $('#switchE').prop('checked', false);
      $('#switchP').prop('checked', false);
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

    $('.myupdate').on('click', function(){
      var $this = $(this)
      var id = $(this).data('id');
      $.confirm({
        title: 'Pass command pop-up',
        content: 'Do you want to proceed ?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: "http://127.0.0.1:8000/pdc/commandes/fromtask/"+id,
                  type: 'POST',
                  beforeSend: function(xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                  },
                  success: function(response){
                      $this.fadeOut(200);
                      $this.closest('tr').children('td:eq(8)').replaceWith('<td>True</td>');
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
