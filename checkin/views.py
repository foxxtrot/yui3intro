from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from pcc2010.checkin.models import Registration
from django.db.models import Q

def index(request):
    try:
        ft = request.session['filter_text']
    except KeyError:
        ft = ""
    registration_list = Registration.objects.filter(Q(full_name__contains = ft) | Q(email__contains = ft)).order_by('full_name')
    return render_to_response('checkin/index.html', {'registration_list': registration_list, 'filter_text': ft})

def checkin(request, registration_id):
    try:
        r = Registration.objects.get(pk = registration_id)
    except Registration.DoesNotExist:
        raise Http404
    r.checkedin = True
    r.save()
    return HttpResponseRedirect('/checkin/')

def filter(request):
    request.session['filter_text'] = request.POST['filter_text']
    return HttpResponseRedirect('/checkin/')

