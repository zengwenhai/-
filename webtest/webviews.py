from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login
from webtest.models import Webcase, Webcasestep
from django.views.decorators.clickjacking import xframe_options_sameorigin
# Create your views here.


# web用例关联
@login_required
def webcase_manage(request):
    username = request.session.get('user', '')
    webcase_list = Webcase.objects.all()
    return render(request, 'webcase_manage.html', {'user': username, 'webcases': webcase_list})


# web测试用例步骤
@login_required
def webcasestep_manage(request):
    username = request.session.get('user', '')
    webcasestep_list = Webcasestep.objects.all()
    return render(request, 'webcasestep_manage.html', {'user': username, 'webcasesteps': webcasestep_list})


@login_required
@xframe_options_sameorigin
def websearch(request):
    username = request.session.get('user', '')
    search_webcasename = request.GET.get('webcasename', '')
    webcase_list = Webcase.objects.filter(webcasename__contains=search_webcasename)
    return render(request, 'webcase_manage.html', {'user': username, 'webcases': webcase_list})


@login_required
@xframe_options_sameorigin
def webstepsearch(request):
    username = request.session.get('user', '')
    search_webcasename = request.GET.get('webcasename', '')
    webcasestep_list = Webcasestep.objects.filter(webcasename__contains=search_webcasename)
    return render(request, 'webcasestep_manage.html', {'user': username, 'webcasessteps': webcasestep_list})