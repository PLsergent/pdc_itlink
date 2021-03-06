$(document).ready(function() {
  // Ajout du bouton delete à la fin de chaque ligne 'month value' donc une ligne
  // sur deux. Sinon ajout un <hr> à la suite
  $("#assign").find('tr:eq(1)').append('<hr>');
  var number = 0;
  var index = 0;
  $('#assign tr').each(function(){
    if (number >= 2){
      if (number % 2 == 0){
        $(this).append($('#deletebutton').html());
        $(this).find('.mydelete').attr('id', index);
        index ++;
      }else{
        $(this).append('<hr>');
      }
    }
    number ++;
  });
  // Défini la valeur du form par défaut dans le form set pour correspondre au
  // mois en cours
  index -= 1;
  var today = new Date();
  var month = today.getMonth()+1;
  var year = today.getFullYear();
  $("#id_form-"+index+"-month_0").val(month);
  $("#id_form-"+index+"-month_1").val(year);

// Lorsque l'on click sur le bouton + on ajoute un form au formset
// On défini le mois et l'année du nv form comme étant celui d'après à celui qui précède
// Gère l'incrémentation des ids et de TOTAL FORMS
  $("#new").on('click', function(){
    var index = $("#id_form-TOTAL_FORMS").val();
    var line = (parseInt(index) + 1) * 2;
    var space = parseInt(line) + 1;
    $('#assign tbody').append($('#template tbody').html().replace(/__prefix__/g, index));
    $("#deletebutton a").attr('id', index);
    $("#assign").find("tr:eq("+line+")").append($('#deletebutton').html());
    $("#assign").find("tr:eq("+space+")").append('<hr>');
    $('#id_form-TOTAL_FORMS').val(parseInt(index) + 1);
    if (month == 12){
      month = 1;
      year ++;
    }else{
      month ++;
    }
    $("#id_form-"+index+"-month_0").val(month);
    $("#id_form-"+index+"-month_1").val(year);
  });

// Lorsque l'on supprime un form du form set
// Si il s'agit du dernier élémént du form set on supprime simplement
// Sinon on met à jour les ids de tous les éléments suivant
  $("#assign").on('click','.mydelete', function(){
    var index = $("#id_form-TOTAL_FORMS").val();
    var elt = $(this).closest('tr');
    if (elt.next().is(":last-child")){
      $("#id_form-TOTAL_FORMS").val(parseInt(index) - 1);
      elt.next().remove();
      elt.remove();
    }else{
      $("#id_form-TOTAL_FORMS").val(parseInt(index) - 1);
      index = $("#id_form-TOTAL_FORMS").val();
      var id = $(this).attr('id');
      var eltiter = elt.next().next();
      elt.next().remove();
      elt.remove();
      var iter = 0;
      total = (index-id)*2;
      while (iter < total){
        if (iter % 2 == 0){
          eltiter.find('th label').attr('for', "id_form-"+id+"-month_0");
          eltiter.find('td .w-month-year').attr({'name': "form-"+id+"-month_0", 'id': "id_form-"+id+"-month_0"});
          eltiter.find('td .w-year').attr({'name': "form-"+id+"-month_1", 'id': "id_form-"+id+"-month_1"});
          eltiter.find('a').attr('id', id);
          iter ++;
          eltiter = eltiter.next();
        }else{
          eltiter.find('th label').attr('for', "id_form-"+id+"-pourcentage");
          eltiter.find('td select').attr({'name': "form-"+id+"-pourcentage", 'id': "id_form-"+id+"-pourcentage"});
          id ++;
          iter ++;
          eltiter = eltiter.next();
        }
      }
    }
  });
});
