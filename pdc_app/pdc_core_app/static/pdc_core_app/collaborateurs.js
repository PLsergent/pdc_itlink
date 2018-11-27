$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 3
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
      tableP.fnFilter('PyWe', 0);
      $('#switchPQ').prop('checked', false);
      $('#switchAll').prop('checked', false);
      $('#switchCQ').prop('checked', false);
    });
    $('#switchPQ').on('change', function filter(){
      tableP.fnFilter('PyQt', 0);
      $('#switchW').prop('checked', false);
      $('#switchAll').prop('checked', false);
      $('#switchCQ').prop('checked', false);
    });
    $('#switchAll').on('change', function filter(){
      tableP.fnFilter('PyWe|PyQt|CPQt', 0, true);
      $('#switchW').prop('checked', false);
      $('#switchPQ').prop('checked', false);
      $('#switchCQ').prop('checked', false);
    });
    $('#switchCQ').on('change', function filter(){
      tableP.fnFilter('CPQt', 0);
      $('#switchW').prop('checked', false);
      $('#switchPQ').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
});
