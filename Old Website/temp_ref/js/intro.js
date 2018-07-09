window.requestAnimFrame = (function(){
  return  window.requestAnimationFrame       ||
          window.webkitRequestAnimationFrame ||
          window.mozRequestAnimationFrame    ||
          function( callback ){
            window.setTimeout(callback, 1000 / 60);
          };
})();

// Utilities
//---

function mapRange(value, srcRange, dstRange){ //(value, array, array)
  if (value < srcRange[0] || value > srcRange[1]){   // value is outside source range return
    return NaN;
  }
  var srcMax = srcRange[1] - srcRange[0],
      dstMax = dstRange[1] - dstRange[0],
      adjValue = value - srcRange[0];
  return (adjValue * dstMax / srcMax) + dstRange[0];
}

function dist( x1, y1, x2, y2 ){
  var xs = (x2 - x1) * (x2 - x1);
  var ys = (y2 - y1) * (y2 - y1);

  return Math.sqrt( xs + ys );
}

function constrain(aNumber, aMin, aMax) {
  return aNumber > aMax ? aMax : aNumber < aMin ? aMin : aNumber;
}

function getAngle( x1, y1, x2, y2 ){
  var deltaY = y2 - y1,
      deltaX = x2 - x1;
      return Math.atan2(deltaY, deltaX) * 180 / Math.PI; // In Degrees
}



// Library
//---

// Particle
function Particle(depth, direction, x, y, width, height) {
  this.image = new Image();
  this.image.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOsAAADICAYAAAAJMhZNAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoTWFjaW50b3NoKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo2MTcwOUFGOUMxNkExMUUyOUE3ODkyRTBEQUE4QkFFMiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo2MTcwOUFGQUMxNkExMUUyOUE3ODkyRTBEQUE4QkFFMiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjYxNzA5QUY3QzE2QTExRTI5QTc4OTJFMERBQThCQUUyIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjYxNzA5QUY4QzE2QTExRTI5QTc4OTJFMERBQThCQUUyIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+vkvdswAAFxhJREFUeNrsnfl2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';
  this.imagealt = new Image();
  this.imagealt.src = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAOsAAADICAYAAAAJMhZNAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuMy1jMDExIDY2LjE0NTY2MSwgMjAxMi8wMi8wNi0xNDo1NjoyNyAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENTNiAoTWFjaW50b3NoKSIgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo2MTcwOUFGREMxNkExMUUyOUE3ODkyRTBEQUE4QkFFMiIgeG1wTU06RG9jdW1lbnRJRD0ieG1wLmRpZDo2MTcwOUFGRUMxNkExMUUyOUE3ODkyRTBEQUE4QkFFMiI+IDx4bXBNTTpEZXJpdmVkRnJvbSBzdFJlZjppbnN0YW5jZUlEPSJ4bXAuaWlkOjYxNzA5QUZCQzE2QTExRTI5QTc4OTJFMERBQThCQUUyIiBzdFJlZjpkb2N1bWVudElEPSJ4bXAuZGlkOjYxNzA5QUZDQzE2QTExRTI5QTc4OTJFMERBQThCQUUyIi8+IDwvcmRmOkRlc2NyaXB0aW9uPiA8L3JkZjpSREY+IDwveDp4bXBtZXRhPiA8P3hwYWNrZXQgZW5kPSJyIj8+SsjPiwAAFzBJREFUeNrsXXlf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';
  this.depth = depth;
  this.direction = direction;
  this.x = x;
  this.y = y;
  this.width = width;
  this.height = height;

  if(this.depth == 'close') {
    this.width = 100;
    this.height = 100;
  } else if(this.depth == 'mid') {
    this.width = 85;
    this.height = 85;
  } else if(this.depth == 'far') {
    this.width = 70;
    this.height = 70;
  }

}

Particle.prototype.update = function(velo, angle){

  this.x = this.x + Math.cos(angle) * velo/3;
  this.y = this.y + Math.sin(angle) * velo/3;

  if( this.x > $window.width() + world.padding ) {
    this.x = -world.padding;
  }
  if( this.y > $window.height() + world.padding ) {
    this.y = -world.padding;
  }
  if( this.x < -world.padding ) {
    this.x = $window.width() + world.padding;
  }
  if( this.y < -world.padding ) {
    this.y = $window.height() + world.padding;
  }

}

Particle.prototype.draw = function(context){

  if(this.depth == 'far'){
    context.globalAlpha = 0.2;
  } else if(this.depth == 'mid') {
    context.globalAlpha = 0.6;
  }
  if(this.direction == 'right') {
      context.drawImage(this.image, this.x, this.y, this.width, this.height);
      context.globalAlpha = 1;
  }else if(this.direction == 'left') {
      context.drawImage(this.imagealt, this.x, this.y, this.width, this.height);
      context.globalAlpha = 1;
  }

  return this;
}

//setup world
var canvas = document.getElementById('canvas-intro'),
    ctx = canvas.getContext('2d'),
    $window = $(window),
    images = [];

var world = {
  padding: 999,
  mousePos: {
    x: $window.width()/2 + 60, // Default mouse position on page load
    y: $window.height()/2
  },
  center: {
    x: $window.width()/2,
    y: $window.height()/2
  },
  angle: function(){
    var a = getAngle(world.mousePos.x, world.mousePos.y, world.center.x, world.center.y),
        radians = a * (Math.PI / 180);
    return radians;
  },
  velocity: function(){
    var d = dist(world.mousePos.x, world.mousePos.y, world.center.x, world.center.y),
        c = constrain(d, 0, $window.width()/2),
        v = mapRange(c, [0,$window.width()/2], [0,5]);
    return v;
  }
}
canvas.width = $window.width();
canvas.height = $window.height() * 0.9;

// Iterator to create 20 particles
for (var i = 0; i < 20; i++) {

    var depth,
        direction = mapRange(Math.random(), [0,1], [0,1]);

    // Assign Depth
    if(i <= 10){
      depth = 'far';
    } else if (i <= 20){
      depth = 'mid';
    } else if (i <= 30){
      depth = 'mid';
    }

    // Assign Direction
    if(direction >= 0.5) {
      direction = 'left';
    } else if(direction <= 0.5) {
      direction = 'right';
    }

    if(images.length == 0){
      var x = mapRange(Math.random(), [0,1], [-world.padding,$window.width()+ world.padding]),
          y = mapRange(Math.random(), [0,1], [-world.padding,$window.height()+ world.padding]),
          image = new Particle(depth, direction, x, y);
      images.push(image);
    } else {
      testIsolation();
    }
    var vvvvvv= 0;
    function testIsolation(){
      vvvvvv = vvvvvv + 1;
      var isIsolated = false,
          testX = mapRange(Math.random(), [0,1], [0,$window.width()]),
          testY = mapRange(Math.random(), [0,1], [0,$window.height()]);


        for (var i = 0; i < images.length; i++) {
          var image = images[i],
              distance = dist(image.x, image.y, testX, testY);

          if(distance < world.padding){
            // console.log('testIsolation return false');
            isIsolated = false;
          } else {
            // console.log('testIsolation return true');
            isIsolated = true;
          }
        };

        if(isIsolated == true){
          var newImage = new Particle(depth, direction, testX, testY);
          images.push(newImage);
          return;
        } else {
          if (vvvvvv < 2000)
          testIsolation();
        else
          return;
        }
    }

};

//draw world
(function animloop(){
    var velocity = world.velocity(),
        angle = world.angle();

    requestAnimFrame(animloop);
    ctx.fillStyle ='#fff';
    ctx.fillRect(0, 0, $window.width(), $window.height());

    for (var i = 0; i < images.length; i++) {
      var depth = images[i].depth;
      if(depth == 'far'){
        images[i].update(velocity/2, angle);
      }else if(depth == 'mid'){
        images[i].update(velocity/1.2, angle);
      }else {
        images[i].update(velocity, angle);
      }
      images[i].draw(ctx);
    };

 })();

 // Events
 canvas.addEventListener('mousemove', function(e){ // mouse position calculation based on when mouse moves onto canvas
  var rect = canvas.getBoundingClientRect();
  world.mousePos = {
    x: e.clientX - rect.left,
    y: e.clientY - rect.top
  }
 });