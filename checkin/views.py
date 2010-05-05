from django.http import HttpResponse
from django.shortcuts import render_to_response
from pcc2010.checkin.models import Registration

def index(request):
    registration_list = Registration.objects.all().order_by('full_name')
    return render_to_response('checkin/index.html', {'registration_list': registration_list})
