$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 4
      }
    }
    );
    var table = new $.fn.dataTable.Api( '#myTable' );

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
    } );

    $('#switchAll').prop('checked', true);
    $('#switchW').prop('checked', false);
    $('#switchPQ').prop('checked', false);
    $('#switchCQ').prop('checked', false);


    $('#switchW').on('change', function filter(){
      tableP.fnFilter('PyWe', 1);
      $('#switchPQ').prop('checked', false);
      $('#switchAll').prop('checked', false);
      $('#switchCQ').prop('checked', false);
    });
    $('#switchPQ').on('change', function filter(){
      tableP.fnFilter('PyQt', 1);
      $('#switchW').prop('checked', false);
      $('#switchAll').prop('checked', false);
      $('#switchCQ').prop('checked', false);
    });
    $('#switchAll').on('change', function filter(){
      tableP.fnFilter('PyWe|PyQt|CPQt', 1, true);
      $('#switchW').prop('checked', false);
      $('#switchPQ').prop('checked', false);
      $('#switchCQ').prop('checked', false);
    });
    $('#switchCQ').on('change', function filter(){
      tableP.fnFilter('CPQt', 1);
      $('#switchW').prop('checked', false);
      $('#switchPQ').prop('checked', false);
      $('#switchAll').prop('checked', false);
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
        title: 'Deletion confirm pop-up',
        content: 'Do you want to proceed ?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: "http://127.0.0.1:8000/pdc/collaborateurs/delete/"+id,
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
