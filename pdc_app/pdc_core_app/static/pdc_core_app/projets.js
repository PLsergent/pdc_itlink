$(document).ready( function () {
    $('#myTable').DataTable({
      sScrollX: "100%",
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 7
      }
    }
    );
} );
