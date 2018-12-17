$(document).ready(function() {
  var count = 0;
  $('table > tbody > tr').each(function(){
    var cell = $(this).children('td:eq(4)')
    console.log(cell.text())
    if (cell.text().startsWith("MAJ")){
      cell.prepend('<i class="fas fa-pen-square"></i>');
      cell.addClass("has-background-warning");
    }else if(cell.text().startsWith("Création")){
      cell.prepend('<i class="fas fa-plus-square"></i>');
      cell.addClass("has-background-success");
    }else{
      cell.prepend('<i class="fas fa-trash-alt"></i>');
      cell.addClass("has-background-danger");
    }
  });

  $('table > tbody > tr').hover(function(){
    var cell = $(this).children('td:eq(4)')
    if (cell.text().startsWith("MAJ")){
      $(this).addClass("has-background-warning");
    }else if(cell.text().startsWith("Création")){
      $(this).addClass("has-background-success");
    }else{
      $(this).addClass("has-background-danger");
    }
  }, function(){
    var cell = $(this).children('td:eq(4)')
    if (cell.text().startsWith("MAJ")){
      $(this).removeClass("has-background-warning");
    }else if(cell.text().startsWith("Création")){
      $(this).removeClass("has-background-success");
    }else{
      $(this).removeClass("has-background-danger");
    }
  });
});
