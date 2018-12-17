$(document).ready(function() {
  $('table > tbody > tr').each(function(){
    var cell = $(this).children('td:eq(4)')
    if (cell.text().startsWith("MAJ")){
      $(this).addClass("has-background-warning");
    }else if(cell.text().startsWith("Création")){
      $(this).addClass("has-background-success");
    }else{
      $(this).addClass("has-background-danger");
    }
  });
});
