$(document).ready(function() {
  $("#assign").find('tr:eq(1)').append('<hr>')
  var today = new Date();
  var mm = today.getMonth()+1;
  $("#id_form-0-month_0").val(mm)
});
