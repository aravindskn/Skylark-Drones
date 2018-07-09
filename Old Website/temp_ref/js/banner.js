var speed = 900;
var container =  $('#demo');  
container.each(function() {   
  var elements = $(this).children('div');
  elements.each(function() {      
    var elementOffset = $(this).offset(); 
    var offset = elementOffset.left + elementOffset.top;
    var delay = parseFloat(offset/speed).toFixed(2);
    $(this)
      .attr("style","animation-delay:"+delay+"s");
  });
});
