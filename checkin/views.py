from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from pcc2010.checkin.models import Registration

def index(request):
    registration_list = Registration.objects.all().order_by('full_name')
    return render_to_response('checkin/index.html', {'registration_list': registration_list})

def checkin(request, registration_id):
    try:
        r = Registration.objects.get(pk = registration_id)
    except Registration.DoesNotExist:
        raise Http404
    r.checkedin = True
    r.save()
    return HttpResponseRedirect('/checkin/')
