import requests, time, sys, re
import urllib, zlib
import pymysql

import HTMLTestRunner_PY3
import unittest
from trace import CoverageResults
import json
from idlelib.rpc import response_queue
from time import sleep


HOSTNAME = '127.0.0.1'


class ApiFlow(unittest.TestCase):
    def test_readSQLcase(self):  # 读取数据库中相应的接口用例数据
        sql = 'select id, apiname, apiurl, apimethod, apiparamvalue, apiresult,' \
              'apistatus from apitest_apistep where apitest_apistep.Apitest_id=3'
        conn = pymysql.connect(
            user='root',
            passwd='root',
            host='127.0.0.1',
            port=3306,
            db='autotest'
        )
        cursor = conn.cursor()
        data = cursor.execute(sql)
        info = cursor.fetchmany(data)
        for i in info:
            case_list = []
            case_list.append(i)
        conn.commit()
        cursor.close()
        conn.close()


def urlParam(param):  # 将页面中的&quot解析为"
    param1 = param.replace('&quot', '"')
    return param1


def readRes(res, res_check):
    res = res.decode().replace('":"', '=').replace('":"', '=')
    res_check = res_check.split(';')
    for s in res_check:
        if s in res:
            pass
        else:
            return '错误，返回参数和预期结果不一致' + s
    return 'pass'


def preOrderSN(results):
    global preOrderSN
    regx = '.*"preOrderSN":"(.*)","toHome"'
    pm = re.search(regx, results)
    if pm:
        preOrderSN = pm.group(1).encode('utf-8')
        return preOrderSN
    return False


def TaskId(results):
    global TaskId
    regx = '.*"TaskId":(.*),"PlanId"'  # 左匹配TaskId":，右匹配,"PlanId"
    pm = re.search(regx, results)
    if pm:
        TaskId = pm.group(1).encode('utf-8')
        return TaskId
    return False


def taskNo(param):
    global taskno
    time1 = int(time.time())
    taskNo = 'task_'+str(time1)
    return taskNo


def writeResult(case_id, result):
    result = result.encode('utf-8')
    now = time.strftime("%Y-%m-%d %H:%M:%S")
    sql = "update apitest_apistep set apitest_apistep.apistatus=%s where apitest_apistep.Apitest_id=%s;"
    param = (result, case_id)
    conn = pymysql.connect(
        user='root',
        passwd='root',
        host='127.0.0.1',
        port=3306,
        db='autotest'
    )
    cursor = conn.cursor()
    cursor.execute(sql, param)  # 传入参数执行sql
    conn.commit()
    cursor.close()
    conn.close()


def writeBug():
    pass


def interfaceTest(case_list):
    res_flags = []
    request_url = []
    response = []
    strinfo = re.compile('{TaskId}')
    strinfo1 = re.compile('{AssertId}')
    strinfo2 = re.compile('{assetno}')
    tasknoinfo = re.compile('{taskno}')
    schemainfo = re.compile('{schema}')
    for case in case_list:
        try:
            case_id = case[0]
            interface_name = case[0]
            method = case[3]
            url = case[2]
            param = case[4]
            res_check = case[5]
        except Exception as e:
            return '测试用例格式不正确%s' %e
        if param == '':
            new_url = 'http://' + 'api.test.com.cn' + url
        elif param == 'null':
            new_url = 'http://' + url
        else:
            url = strinfo.sub(TaskId, url)
            param = strinfo.sub(TaskId, param)
            param = tasknoinfo.sub(taskno, param)
            new_url = 'http://127.0.0.1' + url
            request_url.append(new_url)
        if method.upper() == 'GET':
            headers = {'Authorization': '', 'Content-Type': 'application/json'}
            if '=' in urlParam(param):
                data = None
                print(str(case_id)+'request is get' + new_url.encode('utf-8')+'?'+urlParam(param).encode('utf-8'))
                results = requests.get(new_url+'?'+urlParam(param), data, headers=headers).text
                print('response is get'+results.encode('utf-8'))
                response.append(results)
                res = readRes(results, res_check)
            else:
                print('response is get'+new_url+'body is '+urlParam(param))
                data = None
                req = urllib.request.Request(url=new_url, data=data, headers=headers, method='GET')
                results = urllib.resquest.urlopen(req).read()
                print('response is get')
                print(results)
                res = readRes(results, res_check)
                if res == 'pass':
                    writeResult(case_id, '1')
                    res_flags.append('pass')
                else:
                    res_flags.append('fail')
                    writeResult(case_id, '0')


if __name__ == "__main__":
    #now = time.strftime("%Y-%m-%d-%H_%M_%s", time.localtime(time.time()))
    testunit = unittest.TestSuite()
    testunit.addTest(ApiFlow('test_readSQLcase'))
    filename = r'D:\autotest\apitest\templates\apitest_report.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner_PY3.HTMLTestRunner(
        stream=fp,
        title='流程接口测试报告',
        description='流程场景接口'
    )
    runner.run(testunit)
    print('Done')