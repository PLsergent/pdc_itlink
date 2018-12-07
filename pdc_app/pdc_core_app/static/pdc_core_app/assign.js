$(document).ready(function() {
  $('#id_form-TOTAL_FORMS').val(1);
  $("#assign").find('tr:eq(1)').append('<hr>')
  $("#assign").find('tr:eq(2)').append($('#deletebutton').html())
  $("#assign").find('tr:eq(3)').append('<hr>')

  var today = new Date();
  var month = today.getMonth()+1;
  var year = today.getFullYear();
  $("#id_form-0-month_0").val(month);
  $('#id_form-0-month_1').val(year)

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
      total = (index-id)*2
      while (iter < total){
        if (iter % 2 == 0){
          eltiter.find('th label').attr('for', "id_form-"+id+"-month_0");
          eltiter.find('td .w-month-year').attr({'name': "form-"+id+"-month_0", 'id': "id_form-"+id+"-month_0"});
          eltiter.find('td .w-year').attr({'name': "form-"+id+"-month_1", 'id': "id_form-"+id+"-month_1"})
          eltiter.find('a').attr('id', id)
          iter ++;
          eltiter = eltiter.next()
        }else{
          eltiter.find('th label').attr('for', "id_form-"+id+"-pourcentage");
          eltiter.find('td select').attr({'name': "form-"+id+"-pourcentage", 'id': "id_form-"+id+"-pourcentage"})
          id ++;
          iter ++;
          eltiter = eltiter.next()
        }
      }
    }
  });
});
