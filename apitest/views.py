from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth import authenticate, login
from apitest.models import Apitest, Apistep, Apis
import pymysql
from django.views.decorators.clickjacking import xframe_options_sameorigin
# Create your views here.


def test(request):
    return HttpResponse('hello world')


def login(request):
    if request.POST:
        username = ''
        password = ''
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            request.session['user'] = username  # 登录成功在session中加入用户名
            response = HttpResponseRedirect('/home/')  # 登录成功跳转至home页面

            return response
        else:
            return render(request, 'login.html', {'error': 'username or password is error'})
    return render(request, 'login.html')


@xframe_options_sameorigin
def home(request):
    return render(request, 'home.html')


def logout(request):
    auth.logout(request)
    return render(request, 'login.html')


# 接口管理
@login_required
@xframe_options_sameorigin
def apitest_manage(request):
    apitest_list = Apitest.objects.all()  # 读取所有流程接口的数据
    username = request.session.get('user', '')  # 读取浏览器登录session中保存的用户名
    return render(request, 'apitest_manage.html', {'user': username, 'apitests': apitest_list})


# 接口步骤管理
@login_required
@xframe_options_sameorigin
def apistep_manage(request):
    username = request.session.get('user', '')
    apistep_list = Apistep.objects.all()
    return render(request, 'apistep_manage.html', {'user': username, 'apisteps': apistep_list})


# 单一接口管理
@login_required
@xframe_options_sameorigin
def apis_manage(request):
    username = request.session.get('user', '')
    apis_list = Apis.objects.all()
    return render(request, 'apis_manage.html', {'user': username, 'apiss': apis_list})


# 测试报告
@login_required
@xframe_options_sameorigin
def test_report(request):
    username = request.session.get('user', '')
    apis_list = Apis.objects.all()
    apis_count = Apis.objects.all().count()  # 统计接口数
    conn = pymysql.connect(
        user='root',
        passwd='root',
        host='127.0.0.1',
        port=3306,
        db='autotest'
    )
    cursor = conn.cursor()
    sql_pass = 'select count(id) from apitest_apis where apitest_apis.apistatus=1'  # 获取测试用例通过的sql语句
    pass_row = cursor.execute(sql_pass)
    apis_pass_count = [row[0] for row in cursor.fetchmany(pass_row)][0]
    sql_fail = 'select count(id) from apitest_apis where apitest_apis.apistatus=0'  # 获取测试用例失败的sql语句
    fail_row = cursor.execute(sql_fail)
    apis_fail_count = [row[0] for row in cursor.fetchmany(fail_row)][0]
    cursor.close()
    conn.close()
    return render(request, 'report.html', {'user': username, 'apiss': apis_list,
                                           'apiscounts': apis_count, 'apis_pass_counts': apis_pass_count,
                                           'apis_fail_counts': apis_fail_count})


@xframe_options_sameorigin
def left(request):
    return render(request, 'left.html')


@login_required
@xframe_options_sameorigin
def apisearch(request):
    username = request.session.get('user', '')
    search_apitestname = request.GET.get('apitestname', '')
    apitest_list = Apitest.objects.filter(apitestname__contains=search_apitestname)
    return render(request, 'apitest_manage.html', {'user': username, 'apitests': apitest_list})