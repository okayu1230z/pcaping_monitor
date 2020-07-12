from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse
from datetime import datetime, timedelta
import subprocess
import calendar
from dateutil.relativedelta import relativedelta
import time

class IndexView(generic.TemplateView):
    template_name = "index.html"

def myFunk(req):
    return HttpResponse('This is Admin Page!')

def ping(address):
    cmd = "ping " + address + " -c 1"
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode()
    print(result)
    flag = False if "100% packet loss" in result else True
    return flag

def getTodayList(time):
    cmd = "du -m /mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/" + time.strftime("%d") + "/* | sort -k 2,2"
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode()
    resultList = result.split('\n')[:-1]
    tmpList = []

    for hour in range(time.hour):
        strSearchHour = "0" + str(hour) if hour < 10 else str(hour)
        searchFile = "/mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/" + time.strftime("%d") + "/" + strSearchHour
        searchFlag = False
        for r in resultList:
            mb, dirname = r.split('\t')
            if searchFile in dirname[0:(len(str(searchFile)))]:
                searchFlag = True
                tmpList.append(int(mb))
                break
        if searchFlag == False:
            tmpList.append(0)
    return tmpList

def getYesterdayList(time):
    time = time - timedelta(days=1)
    cmd = "du -m /mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/" + time.strftime("%d") + "/* | sort -k 2,2"
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode()
    resultList = result.split('\n')[:-1]
    tmpList = []
    for hour in range(24):
        strSearchHour = "0" + str(hour) if hour < 10 else str(hour)
        searchFile = "/mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/" + time.strftime("%d") + "/" + strSearchHour
        searchFlag = False
        for r in resultList:
            mb, dirname = r.split('\t')
            if searchFile in dirname[0:(len(str(searchFile)))]:
                searchFlag = True
                tmpList.append(int(mb))
                break
        if searchFlag == False:
            tmpList.append(0)
    return tmpList

def getThisMonth(time):
    cmd = "du -m /mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/* | sort -k 2,2"
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode()
    resultList = result.split('\n')[:-1]
    tmpList = []
    for day in range(1, time.day+1):
        strSearchDay = "0" + str(day) if day < 10 else str(day)
        searchDir = "/mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/" + strSearchDay
        searchFlag = False
        for r in resultList:
            mb, dirname = r.split('\t')
            if searchDir in dirname[0:(len(str(searchDir)))]:
                searchFlag = True
                tmpList.append(int(mb))
                break
        if searchFlag == False:
            tmpList.append(0)
    return tmpList

def getLastMonth(time):
    time = time - relativedelta(months=1)
    cmd = "du -m /mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/* | sort -k 2,2"
    result = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0].decode()
    resultList = result.split('\n')[:-1]
    tmpList = []
    for day in range(1, calendar.monthrange(time.year, time.month)[1]+1):
        strSearchDay = "0" + str(day) if day < 10 else str(day)
        searchDir = "/mnt/sdfs/" + str(time.year) + "/" + time.strftime("%m") + "/" + strSearchDay
        searchFlag = False
        for r in resultList:
            mb, dirname = r.split('\t')
            if searchDir in dirname[0:(len(str(searchDir)))]:
                searchFlag = True
                tmpList.append(int(mb))
                break
        if searchFlag == False:
            tmpList.append(0)
    return tmpList

def myIntexView(req):
    time1 = datetime.now()
    todayList = getTodayList(time1)
    todayList = list(map(lambda x: x/1000, todayList))

    yesterdayList = getYesterdayList(time1)
    yesterdayList = list(map(lambda x: x/1000, yesterdayList))

    thisMonthList = getThisMonth(time1)
    thisMonthList = list(map(lambda x: x/1000, thisMonthList))

    lastMonthList = getLastMonth(time1)
    lastMonthList = list(map(lambda x: x/1000, lastMonthList))

    natAlive = ping("8.8.8.8")
    tcpAlive = ping("8.8.8.8")
    nas1Alive = ping("8.8.8.8")
    nas2Alive = ping("8.8.8.8")

    myParam = {
        'datetime': time.strftime("%Y/%m/%d %a %H:%M:%S %p"),
        'natAlive': natAlive,
        'tcpAlive': tcpAlive,
        'nas1Alive': nas1Alive,
        'nas2Alive': nas2Alive,
        'todayList': todayList,
        'yesterdayList' : yesterdayList,
        'thisMonthList' : thisMonthList,
        'lastMonthList' : lastMonthList
    }
    return render (req, 'index.html', myParam)