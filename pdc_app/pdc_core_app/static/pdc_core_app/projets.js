$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      sScrollX:     "100%",
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      orderFixed: [[ 5, "asc" ],[4, "asc"]],
      fixedColumns: {
        leftColumns: 9,
        rightColumns: 2
      },
  });

    var table = new $.fn.dataTable.Api( '#myTable' );

    $('a.toggle').on( 'click', function (e) {
       e.preventDefault();
       var column = table.column( $(this).attr('data-column') );
       var getIcon = this.querySelector("#icon");
       if (column.visible()){
         column.visible(false);
         getIcon.classList.remove('fa-eye');
         getIcon.classList.add('fa-eye-slash');
       }
       else{
         column.visible(true);
         getIcon.classList.remove('fa-eye-slash');
         getIcon.classList.add('fa-eye');
       }
   } );

   $('a.toggle-all').on( 'click', function(){
     var list = [3, 6, 7, 8];
     var getAllIcon = document.querySelectorAll("#icon");
     for (var i in list){
       var column = table.column(list[i]);
       if (getAllIcon[0].classList.contains('fa-eye')){
         if (column.visible()){
           column.visible(false);
         }
         else{}
       }else{
         if (!column.visible()){
           column.visible(true);
         }else{}
       }
   }
   if (getAllIcon[0].classList.contains('fa-eye')){
     getAllIcon[0].classList.remove('fa-eye');
     getAllIcon[0].classList.add('fa-eye-slash');
   }else{
     getAllIcon[0].classList.add('fa-eye');
     getAllIcon[0].classList.remove('fa-eye-slash');
   }
     for (i = 1; i < getAllIcon.length; ++i) {
       if (getAllIcon[0].classList.contains('fa-eye')){
         getAllIcon[i].classList.add('fa-eye');
         getAllIcon[i].classList.remove('fa-eye-slash');
       }else{
         getAllIcon[i].classList.remove('fa-eye');
         getAllIcon[i].classList.add('fa-eye-slash');
       }
    }
   } );

    table.cells().every( function () {
        var data = this.data()
        if (!isNaN(data) && data.toString().indexOf('.') != -1){}else{
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
        title: 'Order in pop-up',
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

    $('.tooltip').hover(function(){

      if ($(this).attr('data-tooltip') == ""){
        var total = 0
        var colIndex = table.cell($(this)).index().column
        var collab = $(this).closest('tr').children('td:eq(2)').text();
        table.rows( { filter: 'applied' } ).data().each(function(value, index) {
          if ( value[2] == collab ){
            total += parseInt(value[colIndex])
          }
      });
        $(this).attr('data-tooltip', collab + ":" + total);
      }
    });
    var value = ""
    var projet = ""
    var color = color1
    var color1 = ""
    var color2 = "has-background-grey-lighter"
    var rows = $('#myTable > tbody > tr').each(function(index){
      value_update = $(this).children('td:eq(5)').text()
      projet_udpdate = $(this).children('td:eq(4)').text()
      if (value != value_update || projet != projet_udpdate){
        value = value_update
        projet = projet_udpdate
        if (color == color1){
          color = color2
        }else{
          color = color1
        }
        $(this).addClass(color)
        $(".DTFC_LeftBodyLiner > table > tbody > tr:eq("+index+")").addClass(color)
        $(".DTFC_RightBodyLiner > table > tbody > tr:eq("+index+")").addClass(color)

      }else{
        $(this).addClass(color)
        $(".DTFC_LeftBodyLiner > table > tbody > tr:eq("+index+")").addClass(color)
        $(".DTFC_RightBodyLiner > table > tbody > tr:eq("+index+")").addClass(color)
      }

    });
});
