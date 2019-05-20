function add() {
	if (nombre >= 19) { return }
	last_child.removeEventListener('input', add);
	nombre += 1;
	ul.appendChild(create_li());
	last_child = document.getElementsByTagName('li')[8+nombre];
	last_child.addEventListener('input', add);
}

function del() {
	if (nombre <=0) { return }
	last_child = document.getElementsByTagName('li')[8+nombre];
	last_child.remove();
	nombre -= 1;
}

function create_label() {
	var label = document.createElement('label');
	label.innerText = "Etape "+(nombre+1);
	label.setAttribute('for', 'content-'+nombre);
	return label
}

function create_input() {
	var input = document.createElement('textarea');
	input.setAttribute('id', 'content-'+nombre);
	input.setAttribute('name', 'content-'+nombre);
	input.setAttribute('type', 'text');
	input.setAttribute('class', 'materialize-textarea validate')
	input.setAttribute('required', '');
	return input
}

function create_li() {
	var li = document.createElement('li');
	li.appendChild(create_label());
	li.appendChild(create_input());
	return li
}

function testPage() {
	if (window.location.pathname === "/recettes/new"){
	console.log("new")
	document.onload = document.getElementsByTagName('label')[1].innerText = "Etape "+(nombre+1);
	document.onload = document.getElementsByTagName('textarea')[0].setAttribute('class', 'materialize-textarea validate');
	}
	else{
		console.log('update')
		last_child.remove();
		btn_add.remove();
		btn_less.remove();
		a = document.getElementsByTagName('textarea');
		for (var i = 0; i < a.length; i++){
			document.getElementsByTagName('label')[1+i].innerText = "Etape "+(i+1);
			a[i].setAttribute('class', 'materialize-textarea');
			M.textareaAutoResize(a[i])


		}
	}
}
var nombre = 0;

var ul = document.getElementById('recipe');
var text = document.getElementsByTagName('label')[0];

var btn_add = document.getElementsByClassName('btn')[1];
var btn_less = document.getElementsByClassName('btn')[2];

var last_child = document.getElementsByTagName('li')[8+nombre];

btn_add.addEventListener('click', add); //bouton +
btn_less.addEventListener('click', del); //bouton -
last_child.addEventListener('input', add);

document.onload = testPage();
//Reussir a ajouter des input text