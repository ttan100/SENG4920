
// resize the canvas to fill browser window dynamically
window.addEventListener('resize', draw, false);

function draw() {
	var c = document.getElementsByClassName("meal_drop_circle");
	for (var i = 0; i < c.length; i++) {
		c[i].width = 75;
		c[i].height = 75;
		var ctx = c[i].getContext("2d");
		var centerX = c[i].width / 2;
		var centerY = c[i].height / 2;
		ctx.strokeStyle="#333333";
		ctx.beginPath();
		ctx.arc(centerX, centerY, 37, 0, 2 * Math.PI, false);
		ctx.stroke();
	}
}