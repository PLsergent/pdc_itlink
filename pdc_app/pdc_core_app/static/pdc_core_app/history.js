$(document).ready(function() {

//color for actions cells
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
    }else if(cell.text().startsWith("Suppression")){
      cell.prepend('<i class="fas fa-trash-alt"></i>');
      cell.addClass("has-background-danger");
    }else{
      cell.prepend('<i class="fas fa-recycle"></i>');
      cell.addClass("has-background-info");
    }
  });

// Highlight row when hover
  $('table > tbody > tr').hover(function(){
    var cell = $(this).children('td:eq(4)')
    if (cell.text().startsWith("MAJ")){
      $(this).addClass("has-background-warning");
    }else if(cell.text().startsWith("Création")){
      $(this).addClass("has-background-success");
    }else if(cell.text().startsWith("Suppression")){
      $(this).addClass("has-background-danger");
    }else{
      $(this).addClass("has-background-info");
    }
  }, function(){
    var cell = $(this).children('td:eq(4)')
    if (cell.text().startsWith("MAJ")){
      $(this).removeClass("has-background-warning");
    }else if(cell.text().startsWith("Création")){
      $(this).removeClass("has-background-success");
    }else if(cell.text().startsWith("Suppression")){
      $(this).removeClass("has-background-danger");
    }else{
      $(this).removeClass("has-background-info");
    }
  });
});
