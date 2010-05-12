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
        Y.Array.each(data.data, function(entry) {
            entry.fields.id = entry.pk;
            html += Y.substitute("<li class={checkedin}><a class='checkin_link' href='/checkin/checkin/{id}'>{full_name} &lt;{email}&gt;</a></li>",
                entry.fields,
                function(key, value) {
                    if (key === 'checkedin') {
                        return value ? 'checkedin' : '';
                    }
                    return value;
                });
        })
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
});

YUI().use('node', 'json-parse', 'yui2-progressbar', 'gallery-io-poller', function(Y) {
    var container = Y.Node.create("<div id='progress'></div>"),
        progress;
    Y.one('#bd .yui-g').insert(container, 0);

    progress = new Y.YUI2.widget.ProgressBar().render('progress');
    Y.io.poll(5000, '/checkin/stats', {
        on: {
            modified: function(id, response) {
                var data = Y.JSON.parse(response.responseText);
                progress.set('maxValue', data.total);
                progress.set('value', data.checkedin);
            }
        }
    }).start();
});
