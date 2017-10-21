function allowDrop(ev) {
	ev.preventDefault();
}

function drag(ev) {
	ev.dataTransfer.setData("text", ev.target.id);
}

function get_pos(ev){
    pos = [ev.pageX, ev.pageY];
}

function drop(ev) {
	ev.preventDefault();
	var data = ev.dataTransfer.getData("text");
	var img = document.getElementById(data);
	var canvas = ev.target;
	var ctx = canvas.getContext("2d");
	
	ctx.save();
	ctx.beginPath();
	ctx.arc(canvas.width/2, canvas.height/2, 37, 0, Math.PI*2);
	ctx.closePath();
	ctx.clip();
	
	ctx.drawImage(img, 0, 0, 75, 75);
	
	ctx.beginPath();
	ctx.arc(canvas.width/2, canvas.height/2, 37, 0, Math.PI*2);
	ctx.clip();
	ctx.closePath();
	ctx.restore();
}
