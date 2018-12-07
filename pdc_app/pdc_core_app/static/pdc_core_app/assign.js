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
    var space = parseInt(line) + 1
    $('#assign tbody').append($('#template tbody').html().replace(/__prefix__/g, index));
    $("#assign").find("tr:eq("+line+")").append($('#deletebutton').html())
    $("#assign").find("tr:eq("+space+")").append('<hr>')
    $('#id_form-TOTAL_FORMS').val(parseInt(index) + 1);
    if (month == 12){
      month = 1;
      year ++;
    }else{
      month ++;
    }
    $("#id_form-"+index+"-month_0").val(month);
    $("#id_form-"+index+"-month_1").val(year)
  });
});
