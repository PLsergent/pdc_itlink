$(document).ready( function () {
    var tableP = $('#myTable').dataTable({
      sScrollX:     "100%",
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      orderFixed: [[ 6, "asc" ],[5, "asc"]],
      fixedColumns: {
        leftColumns: 10,
        rightColumns: 2
      },
  });

    var table = new $.fn.dataTable.Api( '#myTable' );
// ====== hide/show columns ======
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
     var list = [4, 7, 8, 9];
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
// ====== Notification =======
$(document).on('click', '.undo', function() {
    $("#undo").addClass('is-hidden');
    return false;
});
// ====== color cells ======
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
// ====== column filter ======
    $('#switchAll').prop('checked', true);
    $('#switchE').prop('checked', false);
    $('#switchP').prop('checked', false);

    $('#switchE').on('change', function filter(){
      tableP.fnFilter('True', 9);
      $('#switchP').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
    $('#switchP').on('change', function filter(){
      tableP.fnFilter('False', 9);
      $('#switchE').prop('checked', false);
      $('#switchAll').prop('checked', false);
    });
    $('#switchAll').on('change', function filter(){
      tableP.fnFilter('True|False', 9, true);
      $('#switchE').prop('checked', false);
      $('#switchP').prop('checked', false);
    });
// ====== Cookie for token csrft ======
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
// ====== Pass command from task ======
    var base_url = new URL("/", "http://127.0.0.1:8000");
    var url_command_fromtask = new URL('pdc/commandes/fromtask/', base_url);
    var url_command_undo = new URL('pdc/history/revert_projet/Commande/', base_url);
    $('.myupdate').on('click', function(){
      var $this = $(this);
      var id = $(this).data('id');
      $.confirm({
        title: 'Order in pop-up',
        content: 'Do you want to proceed ?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: url_command_fromtask + id,
                  type: 'POST',
                  beforeSend: function(xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                  },
                  success: function(response){
                      $this.fadeOut(200);
                      $this.closest('tr').children('td:eq(9)').replaceWith('<td>True</td>');
                      var proj = $this.closest('tr').children('td:eq(5)').text()
                      var ref = $this.closest('tr').children('td:eq(6)').text()
                      table.rows().data().each(function(value, index) {
                        if ( value[5] == proj && value[6] == ref){
                          $(".DTFC_LeftBodyLiner > table > tbody > tr:eq("+index+") > td:eq(1) a.myupdate").fadeOut(200);
                          $(".DTFC_LeftBodyLiner > table > tbody > tr:eq("+index+") > td:eq(9)").replaceWith('<td>True</td>');
                        }
                      });
                      $("#undo").fadeIn().removeClass("is-hidden");
                      $("#undo a").attr("href", url_command_undo + id);
                      setTimeout(function() {
                          $('#undo').addClass("is-hidden");
                      }, 6000);
                  }
              });
            },
            cancel: function () {
                return;
            }
        }
      });
    });
// ====== Delete element ======
    $('.mydelete').on('click', function(){
      var $this = $(this)
      var id = $(this).data('id');
      var row = table.cell($(this)).index().row;
      var idRow = table.rows().eq(0).indexOf(row);
      $.confirm({
        title: 'Deletion pop-up',
        content: 'Do you want to proceed ?',
        buttons: {
            confirm: function () {
              $.ajax({
                  url: "http://127.0.0.1:8000/pdc/collaborateurs/assign/delete/"+id,
                  type: 'POST',
                  beforeSend: function(xhr) {
                      xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                  },
                  success: function(response){
                      $this.closest('tr').fadeOut(500);
                      $("#myTable > tbody > tr:eq("+idRow+")").fadeOut(500);
                      $(".DTFC_RightBodyLiner > table > tbody > tr:eq("+idRow+")").fadeOut(500);
                      $("#undo").fadeIn().removeClass("is-hidden");
                      $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_projet/RepartitionProjet/"+id);
                      setTimeout(function() {
                          $('#undo').addClass("is-hidden");
                      }, 6000);
                  },
                  error: function(xhr, text, code){
                    if(text == 'error' && code == 'Forbidden'){
                      $('.modal').addClass("is-active");
                      $('.modal-card-body').append('403 Forbidden error');
                      $(document).on('click', '.modal-background', function(){
                          $('.modal').removeClass("is-active");
                          $('.modal-card-body').empty();
                      });
                      $(document).on('click', '#modaldelete', function(){
                          $('.modal').removeClass("is-active");
                          $('.modal-card-body').empty();
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
// ====== % in tooltip ======
    $('.tooltip').hover(function(){

      if ($(this).attr('data-tooltip') == ""){
        var total = 0
        var colIndex = table.cell($(this)).index().column
        var collab = $(this).closest('tr').children('td:eq(3)').text();
        table.rows( { filter: 'applied' } ).data().each(function(value, index) {
          if ( value[3] == collab ){
            total += parseInt(value[colIndex])
          }
      });
        $(this).attr('data-tooltip', collab + ":" + total);
      }
    });
// ====== Row color alternation ======
    var value = ""
    var projet = ""
    var color = color1
    var color1 = ""
    var color2 = "has-background-grey-lighter"
    var rows = $('#myTable > tbody > tr').each(function(index){
      value_update = $(this).children('td:eq(6)').text()
      projet_udpdate = $(this).children('td:eq(5)').text()
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
