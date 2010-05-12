YUI().use('node', 'io', 'json-parse', 'substitute', function(Y) {
	var nextLink = Y.one('#next'),
	    prevLink = Y.one('#prev'),
	    checkinList = Y.one('#checkinlist'),
	    rebuildList = function(id, response) {
		var data = Y.JSON.parse(response.responseText),
		    baseHref = location.pathname.replace(/\/page\/\d+$/, ""),
		    i, html;
		if (data.prevPage) {
			prevLink.removeClass('hidden');
			prevLink.set('href', baseHref + '/page/' + data.prevPage);
		} else {
			prevLink.addClass('hidden');
		}
		if (data.nextPage) {
			nextLink.removeClass('hidden');
			nextLink.set('href', baseHref + '/page/' + data.nextPage);
		} else {
			nextLink.addClass('hidden');
		}
		html = "";
		for( i = 0 ; i < data.data.length ; i += 1 ) {
			data.data[i].fields.id = data.data[i].pk;
			html += Y.substitute("<li class={checkedin}><a class='checkin_link' href='/checkin/checkin/{id}'>{full_name} &lt;{email}&gt;</a></li>", data.data[i].fields, function(key, value) {
				if (key === 'checkedin') {
					return value ? 'checkedin' : '';
				}
				return value;
			});
		}
		checkinList.setContent(html);
	};
	Y.on('click', function(ev) {
		Y.log('Next clicked!');
		Y.io(ev.target.get('href'), {
			on: {
				success: rebuildList
			}
		});
		ev.preventDefault();
	}, "#next");
	Y.on('click', function(ev) {
		Y.log('Previous clicked!');
		Y.io(ev.target.get('href'), {
			on: {
				success: rebuildList
			}
		});
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
