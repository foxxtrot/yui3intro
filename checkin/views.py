from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from pcc2010.checkin.models import Registration
from django.db.models import Q

PAGE_LENGTH = 25

def index(request, page_number=1):
    page_number = int(page_number)
    registration_list = Registration.objects.order_by('full_name').all()
    view_data = {
		    'registration_list': registration_list[(page_number-1) * PAGE_LENGTH:(page_number * PAGE_LENGTH) - 1],
		    'filter_text': ""
		}
    if page_number > 1:
	    view_data["prev_page"] = page_number - 1
    if page_number != len(registration_list) / PAGE_LENGTH:
	    view_data["next_page"] = page_number + 1

    view_data["link_prefix"] = "/checkin/page/";

    return render_to_response('checkin/index.html', view_data);

def checkin(request, registration_id):
    try:
        r = Registration.objects.get(pk = registration_id)
    except Registration.DoesNotExist:
        raise Http404
    r.checkedin = True
    r.save()

    
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
    if page_number > 1:
	    view_data["prev_page"] = page_number - 1
    if page_number != len(registration_list) / PAGE_LENGTH:
	    view_data["next_page"] = page_number + 1
	
    view_data["link_prefix"] = "/checkin/filter/%s/page/" % filter_text

    return render_to_response('checkin/index.html', view_data);
