function add() {
	if (nombre >= 19) { return }
	last_child.removeEventListener('input', add);
	nombre += 1;
	ul.appendChild(create_li());
	last_child = document.getElementsByTagName('li')[10+nombre];
	last_child.addEventListener('input', add);
}

function del() {
	last_child = document.getElementsByTagName('li')[10+nombre];
	last_child.remove();
	nombre -= 1;
}

function create_label() {
	var label = document.createElement('label');
	label.innerText = "Etape "+(nombre+1);
	label.setAttribute('for', 'etape-'+nombre);
	return label
}

function create_input() {
	var input = document.createElement('input');
	input.setAttribute('id', 'etape-'+nombre);
	input.setAttribute('name', 'etape-'+nombre);
	input.setAttribute('type', 'text');
	input.setAttribute('required', '');
	return input
}

function create_li() {
	var li = document.createElement('li');
	li.appendChild(create_label());
	li.appendChild(create_input());
	return li
}

var nombre = 0;

var ul = document.getElementById('comment');
var text = document.getElementsByTagName('label')[0];

var btn_add = document.getElementsByClassName('btn')[1];
var btn_less = document.getElementsByClassName('btn')[2];

var last_child = document.getElementsByTagName('li')[10+nombre];

btn_add.addEventListener('click', add); //bouton +
btn_less.addEventListener('click', del); //bouton -
last_child.addEventListener('input', add);

document.onload = document.getElementsByTagName('label')[0].innerText = "Etape "+(nombre+1);

//Reussir a ajouter des input text