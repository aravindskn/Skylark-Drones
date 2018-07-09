$(document).ready(function(){
    makeModal("modal1");
});
function makeModal(divID) {
            var newModal2 = $("<div/>", {
                id: "cont" + divID,
                ontouchend: "touchEnd(event)"
            }).html("<div id='" + divID + "'  class='modal'></div>").addClass("modalCont").appendTo("#crownBanner");
            curveAnim($("#" + divID));           
}
        
function curveAnim(obj) {
    splitDiv(obj);
    var theID = $(obj).attr("id");
    var momArray = $("#" + theID + " .modalMom");
    var theLength = parseInt($("#" + theID + " .modalMom").size());
    TweenMax.set($(obj), {
        css: {
            opacity: 0,
            perspective: 1200,

        }
    });

        
 
  	$( ".modalMom" ).each(function( index ) {
        TweenMax.from($(this), 25, {
                    transformOrigin: "0% 100%",
            bezier:{
            type: "soft",
            values: [{rotationY: -17}, {rotationY: 17}, {rotationY: -17}, {rotationY: 17}, {rotationY: -15}, {rotationY: 10}, {rotationY: -15}, {rotationY: 17}, {rotationY: -17}, {rotationY: 17}, {rotationY: -17}, {rotationY: 17}, {rotationY: -15}, {rotationY: 13}, {rotationY: -15}, {rotationY: 7}]},
            ease: Power1.easeOut,
            delay: index*.08
        });
        var darkObj = $(this).find(".darkSlice");
        TweenMax.from($(darkObj), 25, {
            bezier:{
            type: "soft",
            values: [{opacity: 0}, {opacity: 1}, {opacity: 0}, {opacity: 1}, {opacity: 0}, {opacity: 1}, {opacity: 0}, {opacity: 1}, {opacity: 0}, {opacity: 1}, {opacity: 0}, {opacity: 1}, {opacity: 0}, {opacity: .7}, {opacity: 0}, {opacity: .0}]},
            ease: Power1.easeOut,
            delay: index*.08
        });   
       
       
       });
    TweenMax.set($("#" + theID), {
        opacity:1 
        });

}

function splitDiv(obj) {
    var curve = $(obj);
    var sliceNum = 15;
    var sliceSize = curve.width() / sliceNum;
    var sliceHeight = curve.height();
    var bgURL = curve.css("background-image");
    var darkURL = "http://fc01.deviantart.net/fs70/f/2010/024/c/d/Plain_Background_by_BlackHug.jpg";
    var bgSize = curve.css("background-size");
    for (i = 0; i < curve.width() / sliceSize; i++) {
        var slice = $("<div/>").css({
            width: (curve.width() - (sliceSize * i)),
            left: sliceSize -1
        }).addClass("modalMom").html("<div class='darkSlice' style='width: " + sliceSize + "px; height: " + sliceHeight + "px; background: " + darkURL + " no-repeat; background-size: " + bgSize + ";'></div>" + "<div class='modalSlice' style='width: " + sliceSize + "px; height: " + sliceHeight + "px; background: " + bgURL + " no-repeat; background-size: " + bgSize + ";'></div>");
        TweenMax.set($("#" + $(curve).attr("id") + " .modalSlice:last, #" + $(curve).attr("id") + " .darkSlice:last"), {
            css: {
                backgroundPosition: "-" + (sliceSize * (i - 1)) + "px 0px"
            }
        });
        if (i > 0) {
            slice.appendTo($("#" + $(curve).attr("id") + " .modalMom").last())
        } else {
            slice.appendTo($(obj))
        }
    }
    TweenMax.set($("#" + $(curve).attr("id") + " .modalSlice:last, #" + $(curve).attr("id") + " .darkSlice:last"), {
        css: {
            backgroundPosition: "-" + (sliceSize * sliceNum - (sliceSize)) + "px 0px"
        }
    });
    $("#" + curve.attr("id")).css("background-image", "none");
}

function rnd(min, max) {
	var rnd = Math.floor(Math.random() * (max - min)) + min;
	return rnd;
}
