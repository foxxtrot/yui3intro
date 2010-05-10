YUI().use('node', 'io', function(Y) {
	Y.on('click', function(ev) {
		Y.log('Next clicked!');
		ev.preventDefault();
	}, "#next");
	Y.on('click', function(ev) {
		Y.log('Previous clicked!');
		ev.preventDefault();
	}, "#prev");

	Y.delegate("click", function(ev) {
		ev.preventDefault();
		Y.io(ev.target.get('href'), {
			on: {
				success: function(id, response) {
					var parent = ev.target.get('parentNode').addClass('checkedin');
				}
			}
		});
	}, '#checkinlist', 'a.checkin_link'); 
});
