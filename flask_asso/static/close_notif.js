var btn  = document.getElementById('button-notif');

if (btn){
	btn.addEventListener('click', function() {
		var notif = document.getElementById('notif');
		notif.remove();
	});
}

document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems);
});