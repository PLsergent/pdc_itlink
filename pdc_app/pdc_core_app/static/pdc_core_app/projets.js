$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      sScrollX: "100%",
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 7
      }
    }
    );

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
