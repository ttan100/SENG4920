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
	canvas.getContext("2d").drawImage(img, 
		canvas.width / 2 - img.width / 2,
		canvas.height / 2 - img.height / 2);
}
