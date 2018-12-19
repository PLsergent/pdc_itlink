$(document).ready(function() {
    $('#myTable').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

$(document).ready(function() {
    $('#myTable2').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

$(document).ready(function() {
    $('#myTable3').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

$(document).ready(function() {
    $('#myTable4').DataTable({
      paging:         false,
      order: [0, "asc"]
    });
} );

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
// ===== Notfication ======
    $(document).on('click', '.undo', function() {
        $("#undo").addClass('is-hidden');
        return false;
    });
$(document).ready(function() {

  // ===== Notfication ======
      $(document).on('click', '.undo', function() {
          $("#undo").addClass('is-hidden');
          return false;
      });

  $('#myTable .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.confirm({
    title: 'Deletion pop-up',
    content: 'Do you want to proceed ?',
    buttons: {
        confirm: function () {
          $.ajax({
              url: "http://127.0.0.1:8000/pdc/projets/delete/"+id,
              type: 'POST',
              beforeSend: function(xhr) {
                  xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
              },
              success: function(response){
                  $this.parent().fadeOut(500);
                  $("#undo").fadeIn().removeClass("is-hidden");
                  $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_data/Projet/"+id);
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
        },
    }
  });
  });

  $('#myTable2 .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.confirm({
    title: 'Deletion pop-up',
    content: 'Do you want to proceed ?',
    buttons: {
        confirm: function () {
          $.ajax({
              url: "http://127.0.0.1:8000/pdc/clients/delete/"+id,
              type: 'POST',
              beforeSend: function(xhr) {
                  xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
              },
              success: function(response){
                  $this.parent().fadeOut(500);
                  $("#undo").fadeIn().removeClass("is-hidden");
                  $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_data/Client/"+id);
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
        },
    }
  });
  });

  $('#myTable3 .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.confirm({
    title: 'Deletion pop-up',
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
                  $this.parent().fadeOut(500);
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
        },
    }
  });
  });

  $('#myTable4 .mydelete').on('click', function(){
    var $this = $(this)
    var id = $(this).data('id');
    $.confirm({
    title: 'Deletion pop-up',
    content: 'Do you want to proceed ?',
    buttons: {
        confirm: function () {
          $.ajax({
              url: "http://127.0.0.1:8000/pdc/projets/tache_probable_delete/"+id,
              type: 'POST',
              beforeSend: function(xhr) {
                  xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
              },
              success: function(response){
                  $this.parent().fadeOut(500);
                  $("#undo").fadeIn().removeClass("is-hidden");
                  $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_data/Commande/"+id);
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
        },
    }
  });
  });

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
                    $this.closest('tr').fadeOut(500);
                    $("#undo").fadeIn().removeClass("is-hidden");
                    $("#undo a").attr("href", "http://127.0.0.1:8000/pdc/history/revert_data_bis/Commande/"+id);
                    setTimeout(function() {
                        $('#undo').addClass("is-hidden");
                    }, 6000);
                },
                error: function(xhr, text, code){
                  if(text == 'error' && code == 'Forbidden'){
                    $('.modal').addClass("is-active");
                    $(document).on('click', '.modal-background', function(){
                        $('.modal').removeClass("is-active");
                    });
                    $(document).on('click', '#modaldelete', function(){
                        $('.modal').removeClass("is-active");
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
