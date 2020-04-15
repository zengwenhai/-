from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login
from apptest.models import Appcase, Appcasestep
from django.views.decorators.clickjacking import xframe_options_sameorigin
# Create your views here.


# 用例关联
@login_required
def appcase_manage(request):
    appcase_list = Appcase.objects.all()
    username = request.session.get('user', '')
    return render(request, 'appcase_manage.html', {'user': username, 'appcases': appcase_list})


# app用例测试步骤
@login_required
def appcasestep_manage(request):
    appcasestep_list = Appcasestep.objects.all()
    username = request.session.get('user', '')
    return render(request, 'appcasestep_manage.html', {'user': username, 'appcasesteps': appcasestep_list})


@login_required
@xframe_options_sameorigin
def appsearch(request):
    username = request.session.get('user', '')
    search_appcasename = request.GET.get('appcasename', '')
    appcase_list = Appcase.objects.filter(appcasename__contains=search_appcasename)
    return render(request, 'appcase__manage.html', {'user': username, 'appcases': appcase_list})


@login_required
@xframe_options_sameorigin
def appstepsearch(request):
    username = request.session.get('user', '')
    search_appcasename = request.GET.get('appcasename', '')
    appcasestep_list = Appcase.objects.filter(appcasename__contains=search_appcasename)
    return render(request, 'appcasestep_manage.html', {'user': username, 'appcasessteps': appcasestep_list})