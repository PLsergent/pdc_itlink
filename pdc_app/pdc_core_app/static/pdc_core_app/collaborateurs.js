$(document).ready( function () {
    $('div .loader').addClass('is-hidden');
    //loading stop
    var fntableSP = $('#myTable').dataTable({
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 4
      }
    }
    );
    var fntablePP = $('#myTable2').dataTable({
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 4
      }
    }
    );
    var fntableCM = $('#myTable3').dataTable({
      scrollX:        true,
      scrollCollapse: true,
      paging:         false,
      fixedColumns: {
        leftColumns: 4
      }
    }
    );
    var tableSP = new $.fn.dataTable.Api( '#myTable' );
    var tablePP = new $.fn.dataTable.Api( '#myTable2' );
    var tableCM = new $.fn.dataTable.Api( '#myTable3' );

    var table = tableSP;
    var tableP = fntableSP;
    var table_id = "#myTable"

    $('#all').css('display', 'inline-block');

    $('#myTable_wrapper').wrap('<div id="hide" style="display:block"/>');
    $('#myTable2_wrapper').wrap('<div id="hide2" style="display:none"/>');
    $('#myTable3_wrapper').wrap('<div id="hide3" style="display:none"/>');

    $('#switch_woprobable').prop('checked', true);
    $('#switch_probablep').prop('checked', false);
    $('#switch_maj').prop('checked', false);

// Switch table
    $("#switch_woprobable").on('change', function(){
      if (!$('#switch_woprobable').prop('checked') && !$('#switch_probablep').prop('checked') && !$('#switch_maj').prop('checked')){
        $('#switch_woprobable').prop('checked', true);
      }else{
        table = tableSP;
        tableP = fntableSP;
        table_id = "#myTable"
        $('#hide').fadeIn().css( 'display', 'block' );
        $('#switch_probablep').prop('checked', false);
        $('#hide2').css( 'display', 'none' );
        $('#switch_maj').prop('checked', false);
        $('#hide3').css( 'display', 'none' );
      }
    });

    $("#switch_probablep").on('change', function(){
      if (!$('#switch_probablep').prop('checked') && !$('#switch_woprobable').prop('checked') && !$('#switch_maj').prop('checked')){
        $('#switch_probablep').prop('checked', true);
      }else{
        table = tablePP;
        tableP = fntablePP;
        table_id = "#myTable2"
        $('#hide2').fadeIn().css( 'display', 'block' );
        $('#switch_woprobable').prop('checked', false);
        $('#hide').css( 'display', 'none' );
        $('#switch_maj').prop('checked', false);
        $('#hide3').css( 'display', 'none' );
      }
    });

    $("#switch_maj").on('change', function(){
      if (!$('#switch_maj').prop('checked') && !$('#switch_probablep').prop('checked') && !$('#switch_woprobable').prop('checked')){
        $('#switch_maj').prop('checked', true);
      }else{
        table = tableCM;
        tableP = fntableCM;
        table_id = "#myTable3"
        $('#hide3').fadeIn().css( 'display', 'block' );
        $('#switch_probablep').prop('checked', false);
        $('#hide2').css( 'display', 'none' );
        $('#switch_woprobable').prop('checked', false);
        $('#hide').css( 'display', 'none' );
      }
    });
// inital color cell
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

    $(document).on('change', "#switch_maj, #switch_woprobable, #switch_probablep", function(){
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
    });

// Hide Show columns
    $('#switchAll').prop('checked', true);
    $('#switchW').prop('checked', false);
    $('#switchPQ').prop('checked', false);
    $('#switchCQ').prop('checked', false);


    $('#switchW').on('change', function filter(){
      if (!$('#switchW').prop('checked')){
        tableP.fnFilter('PyWe|PyQt|CPQt', 1, true);
        $('#switchAll').prop('checked', true);
      }else{
        tableP.fnFilter('PyWe', 1);
        $('#switchPQ').prop('checked', false);
        $('#switchCQ').prop('checked', false);
        $('#switchAll').prop('checked', false);
      }
    });
    $('#switchPQ').on('change', function filter(){
      if (!$('#switchPQ').prop('checked')){
        tableP.fnFilter('PyWe|PyQt|CPQt', 1, true);
        $('#switchAll').prop('checked', true);
      }else{
        tableP.fnFilter('PyQt', 1);
        $('#switchW').prop('checked', false);
        $('#switchCQ').prop('checked', false);
        $('#switchAll').prop('checked', false);
      }
    });
    $('#switchAll').on('change', function filter(){
      if (!$('#switchAll').prop('checked')){
        tableP.fnFilter('XXX', 1);
      }else{
        tableP.fnFilter('PyWe|PyQt|CPQt', 1, true);
        $('#switchW').prop('checked', false);
        $('#switchPQ').prop('checked', false);
        $('#switchCQ').prop('checked', false);
      }
    });
    $('#switchCQ').on('change', function filter(){
      if (!$('#switchCQ').prop('checked')){
        tableP.fnFilter('PyWe|PyQt|CPQt', 1, true);
        $('#switchAll').prop('checked', true);
      }else{
        tableP.fnFilter('CPQt', 1);
        $('#switchW').prop('checked', false);
        $('#switchPQ').prop('checked', false);
        $('#switchAll').prop('checked', false);
      }
    });

    // ====== Notification =======
    $(document).on('click', '.undo', function() {
        $("#undo").addClass('is-hidden');
        return false;
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

// Delete button
    $('.mydelete').on('click', function(){
      var $this = $(this)
      var id = $(this).data('id');
      var row = table.cell($(this)).index().row;
      var idRow = table.rows().eq(0).indexOf(row);
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
                      $("#hide .DTFC_LeftBodyLiner > table > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#hide2 .DTFC_LeftBodyLiner > table > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#hide3 .DTFC_LeftBodyLiner > table > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#myTable > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#myTable2 > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#myTable3 > tbody > tr:eq("+idRow+")").fadeOut(250);
                      $("#undo").fadeIn().removeClass("is-hidden");
                      $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_collab/Collaborateur/"+id);
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
                    }else{
                      $('.modal').addClass("is-active");
                      $('.modal-card-body').append('500 protected error, this object is link to protected data.');
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
  });
