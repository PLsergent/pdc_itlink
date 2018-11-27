$(document).ready( function () {
    $('#myTable').DataTable({
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
} );
