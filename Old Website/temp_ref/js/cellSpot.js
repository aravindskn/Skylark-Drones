jQuery(function( $ ){
  focusInterval();
  var focusIntervalID = window.setInterval(focusInterval, 10000);
});

function focusInterval() {
  window.setTimeout(function(){
    focusCell(1);
  }, 0);
  window.setTimeout(function(){
    focusCell(2);
  }, 3300);
  window.setTimeout(function(){
    focusCell(3);
  }, 6600);
}

function focusCell(step) {
  $cell = $('.cell');
  $crosshair = $('.cell-target-crosshair');
  $outerCircle = $('.cell-target-circle.outer .svg-circle');

  if (step == 1) { 
    $cell.css({ 'filter' : 'blur(4px)', '-webkit-filter' : 'blur(4px)', 'width' : '120px', 'left' : '44.8%', 'top' : '44.8%' });
    $crosshair.css({ 'transform' : 'rotate(0deg)', '-webkit-transform' : 'rotate(0deg)' });
    $outerCircle.css({ 'transform' : 'scale(1)', '-webkit-transform' : 'scale(1)' });
  } else if (step == 2) {
    $cell.css({ 'filter' : 'blur(2px)', '-webkit-filter' : 'blur(2px)', 'width' : '115px', 'left' : '44.9%', 'top' : '44.9%' });
    $crosshair.css({ 'transform' : 'rotate(45deg)', '-webkit-transform' : 'rotate(45deg)' });
    $outerCircle.css({ 'transform' : 'scale(0.9)', '-webkit-transform' : 'scale(0.9)' });
  } else if (step == 3) {
    $cell.css({ 'filter' : 'blur(0px)', '-webkit-filter' : 'blur(0px)', 'width' : '110px','left' : '45%', 'top' : '45%' });
    $crosshair.css({ 'transform' : 'rotate(90deg)', '-webkit-transform' : 'rotate(90deg)' });
    $outerCircle.css({ 'transform' : 'scale(0.8)', '-webkit-transform' : 'scale(0.8)' });
  }
}