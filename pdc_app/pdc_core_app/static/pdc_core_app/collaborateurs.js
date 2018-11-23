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
} );
