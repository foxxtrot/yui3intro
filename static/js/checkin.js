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
        Y.Array.each(data.data, function(entry) {
          entry.fields.id = entry.pk;
          html += "<li class=" + (entry.fields.checkedin ? 'checkedin' : '') +
                  "><a class='checkin_link' href='/checkin/checkin/" +
                  entry.pk + "'>" + entry.fields.full_name + " &lt;" +
                  entry.fields.email + "&gt;</a></li>";
        });
        checkinList.setContent(html);
    };

nextLink.on('click', function(ev) {
  Y.log('Next clicked!');
  Y.io(ev.target.get('href'), {
    on: {
      success: rebuildList
    }
  });
  ev.preventDefault();
});

prevLink.on('click', function(ev) {
  Y.log('Previous clicked!');
  Y.io(ev.target.get('href'), {
    on: {
      success: rebuildList
    }
  });
  ev.preventDefault();
});

Y.on('keyup', function(ev) {
  var value = ev.target.get('value'), url;
  Y.log('Change Event: ' + value);
  if (value !== '') {
    url = '/checkin/filter/' + value;
  } else {
    url = '/checkin/';
  }
  Y.io(url, {
    on: {
      success: rebuildList
    }
  });
}, "#filter_text");

Y.one('#filter_text').get('parentNode').one('input[type=submit]').remove();

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

/*
YUI().use('node', 'json-parse', 'yui2-progressbar', 'gallery-io-poller', 'overlay', 'substitute', function(Y) {
    var container = Y.Node.create("<div id='progress'></div>"),
        progress, overlay;
    Y.one('#bd .yui-g').insert(container, 0);
    Y.one('#bd').insert('<div id="overlay"></div>');
    overlay = new Y.Overlay();
    overlay.render('#overlay');
    overlay.hide();
    progress = new Y.YUI2.widget.ProgressBar().render('progress');
    Y.io.poll(5000, '/checkin/stats', {
        on: {
            modified: function(id, response) {
                var data = Y.JSON.parse(response.responseText);
                progress.set('maxValue', data.total);
                progress.set('value', data.checkedin);

                overlay.set('bodyContent', Y.substitute('<ul><li>Checked-in: {checkedin}</li><li>Total Registrations: {total}</li></ul>',
                    data));
            }
        }
    }).start();

    container.on('mouseover', function(ev) {
        overlay.show();
    });

    container.on('mouseout', function(ev) {
        overlay.hide();
    });
});
*/
