$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      sScrollX: "100%",
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 7
      },
    }
    );
    var table = new $.fn.dataTable.Api( '#myTable' );

    table.cells().every( function () {
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
    } );

    $('#switchAll').prop('checked', true);
    $('#switchE').prop('checked', false);
    $('#switchP').prop('checked', false);

    $('#switchE').on('change', function filter(){
      tableP.fnFilter('True', 6);
      $('#switchP').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
    $('#switchP').on('change', function filter(){
      tableP.fnFilter('False', 6);
      $('#switchE').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
    $('#switchAll').on('change', function filter(){
      tableP.fnFilter('True|False', 6, true);
      $('#switchE').prop('checked', false);
      $('#switchP').prop('checked', false);
    });
});
