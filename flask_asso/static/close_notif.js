var btn  = document.getElementById('button-notif');

if (btn){
	btn.addEventListener('click', function() {
		var notif = document.getElementById('notif');
		notif.remove();
	});
}