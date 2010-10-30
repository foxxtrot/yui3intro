from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core import serializers
from django.shortcuts import render_to_response
from yui3intro.checkin.models import Registration
from django.db.models import Q
from yui3intro.checkin.utilities import getNextPageNumber, getPrevPageNumber
import simplejson as json

PAGE_LENGTH = 25

def index(request, page_number=1):
    page_number = int(page_number)
    registration_list = Registration.objects.order_by('full_name').all()
    view_data = {
            'registration_list': registration_list[(page_number-1) * PAGE_LENGTH:(page_number * PAGE_LENGTH) - 1],
            'filter_text': ""
        }

    view_data["prev_page"] = getPrevPageNumber(page_number)
    view_data["next_page"] = getNextPageNumber(page_number, len(registration_list), PAGE_LENGTH)
    view_data["link_prefix"] = "/checkin/page/";

    if request.is_ajax():
        registrations_json = serializers.serialize('json', view_data["registration_list"]);
        jsonText = json.dumps({
                'nextPage': view_data["next_page"],
                'prevPage': view_data["prev_page"]
            })
        jsonText = jsonText[0:len(jsonText)-1] + ',"data":' + registrations_json + '}'
        return HttpResponse(jsonText)
    return render_to_response('checkin/index.html', view_data);

def checkin(request, registration_id):
    try:
        r = Registration.objects.get(pk = registration_id)
    except Registration.DoesNotExist:
        raise Http404
    r.checkedin = True
    r.save()

    if request.is_ajax():
        return HttpResponse(json.dumps({'id': registration_id, 'checkedin': True}))
    else:
        if request.META["HTTP_REFERER"]:
            return HttpResponseRedirect(request.META["HTTP_REFERER"])
        else:
            return HttpResponseRedirect('/checkin/')

def filter(request, filter_text = None, page_number = 1):
    if filter_text == None:
        return HttpResponseRedirect('/checkin/filter/%s' % request.POST['filter_text'])

    page_number = int(page_number)

    registration_list = Registration.objects.filter(Q(full_name__contains = filter_text) | Q(email__contains = filter_text)).order_by('full_name')
    view_data = {
            'registration_list': registration_list[(page_number-1) * PAGE_LENGTH:(page_number * PAGE_LENGTH) - 1],
            'filter_text': filter_text
        }

    view_data["prev_page"] = getPrevPageNumber(page_number)
    view_data["next_page"] = getNextPageNumber(page_number, len(registration_list), PAGE_LENGTH)
    view_data["link_prefix"] = "/checkin/filter/%s/page/" % filter_text

    if request.is_ajax():
        registrations_json = serializers.serialize('json', view_data["registration_list"]);
        jsonText = json.dumps({
                'nextPage': view_data["next_page"],
                'prevPage': view_data["prev_page"]
            })
        jsonText = jsonText[0:len(jsonText)-1] + ',"data":' + registrations_json + '}'
        return HttpResponse(jsonText)
    return render_to_response('checkin/index.html', view_data);

def stats(request):
    #if not request.is_ajax():
    #    return Http404A
    jsonText = json.dumps({
        'total': Registration.objects.count(),
        'checkedin': Registration.objects.exclude(checkedin__exact = False).count()
    });
    return HttpResponse(jsonText);
