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
	var dx = pos[0] - img.offsetLeft;
	var dy = pos[1] - img.offsetTop;
	ev.target.getContext("2d").drawImage(document.getElementById(data), ev.pageX - dx, ev.pageY - dy);
}