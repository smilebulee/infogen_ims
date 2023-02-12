from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse

from django.core.paginator import Paginator
from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_exempt
# from .models import TB_EMP,Cd

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, is_password_usable
from main.helpers import ajax_login_required

import requests
import logging
import json
import ast

logger = logging.getLogger(__name__)

# 공지사항 파일업로드 임시추가
from .models import Document
from .forms import DocumentForm


class Dili_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/index.html'

        return render(request, template_name)


def scheduleMgmt(request):
    template_name = 'dili/diliScheduleMgmt.html'

    return render(request, template_name)


class scheduleMgmtPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/diliScheduleMgmtPop.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)

class mariatest(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/mariatest.html'
        # 화면 호출
        r = requests.get('http://dili_api:5006/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)



def getMaria(request):
    param = json.loads(request.GET['param'])

    logger.info("Start")
    logger.info(param)
    logger.info("End")

    # api 호출
    r = requests.get('http://dili_api:5006/mariatestDB')
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def getYryMgmt(request):
    param = json.loads(request.GET['param'])

    logger.info("Start")
    logger.info(param)
    logger.info("End")

    # api 호출
    r = requests.get('http://dili_api:5006/yryMgmt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def getHldyMgmt(request):
    logger.info("getHldyMgmt Start")
    param = json.loads(request.GET['param'])


    logger.info(param)
    logger.info("getHldyMgmt End")

    # api 호출
    r = requests.get('http://dili_api:5006/hldyMgmt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def getWeekGridData(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/weekGridData', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getApvlInfo(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlInfo', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getMonthGridData(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/monthGridData', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getWrkTimeInfoByEml(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/wrkTimeInfoByEml', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getTotalWrktm(request):
    param = json.loads(request.GET['param'])

    logger.info(param)

    # api 호출
    r = requests.get('http://dili_api:5006/totalWrktm', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getEmpList(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empList', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getEmpInfo(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empInfo', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getEmpName(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empName', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


def getEmpDept(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empDept', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


def getEmpDeptGm(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empDeptGm', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getEmpDeptPr(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empDeptPr', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


class wrkApvlReq(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqWrkSub.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)
    
class yryApvlReq(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqYrySub.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)


class apvlReqPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqPop.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)


class yryApvlReqPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/yryApvlReqPopup.html'

        logger.info("yryApvlReqPop")
        logger.info(request)
        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)


class apvlReqBfrPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqBfrPop.html'

        return render(request, template_name)

class apvlReqBfrChkPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqBfrChkPop.html'

        return render(request, template_name)

def getDuplApvlReqCnt(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/duplApvlReqCnt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getDuplApvlYryReqCnt(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/duplApvlYryReqCnt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getDuplWrkCnt(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/duplWrkCnt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


def getWrkTm(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/wrkTm', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


class apvlReqLtrPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqLtrPop.html'

        return render(request, template_name)


class apvlAcptPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlAcptPop.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)



class noticeLst(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/noticeLst.html'


        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)


def getNoticeLst(request):
    param = json.loads(request.GET['param'])
    logger.info("getNoticeLst : dili/views.py")
    logger.info(param)

    datas = {
        'category': param['category'],
        'searchStr': param['searchStr']
    }

    logger.info(datas)

    # api 호출
    r = requests.get('http://dili_api:5006/noticeLst', params=datas)
    logger.info("sql 끝")
    paginator = Paginator(r.json(), 10)
    logger.info("----------------")
    logger.info(paginator)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")

    result = paginator.get_page(param['page'])

    logger.info(result)

    data = {
        'list': list(result.object_list),
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'page': result.number,
        'has_next': result.has_next(),
        'has_prev': result.has_previous()
    }

    # return JsonResponse(r.json())
    return JsonResponse(data)


def getNoticePopCnt(request):
    param = json.loads(request.GET['param'])

    logger.info(param)

    params = {
    }

    r = requests.get('http://dili_api:5006/noticePopCnt', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


def getNoticePopUp(request):
    param = json.loads(request.GET['param'])

    logger.info(param)

    params = {
    }
    # param X

    r = requests.get('http://dili_api:5006/noticePopUp', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


def getNoticeMjrCnt(request):
    param = json.loads(request.GET['param'])

    logger.info(param)

    params = {
    }
    #param X

    r = requests.get('http://dili_api:5006/noticeMjrCnt', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


class noticeDtl(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/noticeDtl.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)

def getNoticeOne(request):
    param = json.loads(request.GET['param'])

    logger.info(param)
    logger.info("공지사항 상세정보")

    params = {
        'postId': param['postId'],
    }

    r = requests.get('http://dili_api:5006/noticeOne', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def noticeSave(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        #logger.info(row + ':' + param[row])
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/noticeSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def noticeDelete(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        #logger.info(row + ':' + param[row])
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/noticeDelete', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class empMgmt(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/empMgmt.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)

class empMgmtPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/empMgmtPop.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)
        # return render(request, template_name, rr)


def getWrkApvlReq(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/wrkApvlReq', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


def saveApvlReq(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        logger.info(row)
        logger.info(row + ':' + param[row])
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/saveApvlReq', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def saveApvlAcpt(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        logger.info(row)
        logger.info(row + ':' + param[row])
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/saveApvlAcpt', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

#공통 코드 조회
def retrieveCmmCd(request):
    param = json.loads(request.GET['param'])

    logger.info("retrieveCmmCd Start")
    logger.info(param)
    logger.info("retrieveCmmCd End")

    # api 호출
    r = requests.get('http://dili_api:5006/retrieveCmmCd', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

class scheduleStatLst(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/scheduleStatLst.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)

def getScheduleStatLst(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/scheduleStatLst', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)



class apvlReqHist(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/apvlReqHist.html'

        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }

        return render(request, template_name)
        # return render(request, template_name, rr)

def getApvlReqHist(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlReqHist', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(ast.literal_eval(r.json()))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getApvlReqHistDetl(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlReqHistDetl', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getApvlWrkReqHistDetl(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlReqWrkHistDetl', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getApvlAcptHist(request):
    param = json.loads(request.GET['param'])

    logger.info("getApvlAcptHist Parameters Start")
    logger.info(param)
    logger.info("getApvlAcptHist Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/apvlAcptHist', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)


def getCalendarData(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/calendarData', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))
    return JsonResponse(r.json(), safe=False)

def saveYryApvlReq(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(type(json.dumps(param)))
    logger.info("Parameters End")

    r = requests.post('http://dili_api:5006/saveYryApvlReq', data=json.dumps(param), headers = {'Content-Type': 'application/json; charset=utf-8'})
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def saveYryApvlCncl(request):
    param = json.loads(request.POST['param'])

    logger.info("saveYryApvlCncl Parameters Start")
    logger.info(type(json.dumps(param)))
    logger.info("saveYryApvlCncl Parameters End")

    r = requests.post('http://dili_api:5006/saveYryApvlCncl', data=json.dumps(param), headers = {'Content-Type': 'application/json; charset=utf-8'})
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

# 공지사항 파일업로드 임시추가
def my_view(request):
    print(f"Great! You're using Python 3.6+. If you fail here, use the right version.")
    message = 'Upload as many files as you want!'
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return redirect('dili_api:noticeDtl')
        else:
            message = 'The form is not valid. Fix the following error:'
    else:
        form = DocumentForm()  # An empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    context = {'documents': documents, 'form': form, 'message': message}
    return render(request, 'dili/noticeDtl.html', context)

#출근시간 저장
def saveStrtTm(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")


    r = requests.post('http://dili_api:5006/insertStrtTm', data=json.dumps(param))

    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

#퇴근시간 저장
def saveEndTm(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")


    r = requests.post('http://dili_api:5006/updateEndTm', data=json.dumps(param))

    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

#근무시간 확정
def saveWrkTimeConfirm(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    r = requests.post('http://dili_api:5006/updateWrkTimeConfirm', data=json.dumps(param))

    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

#근무시간 생성
def saveWrkGen(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    r = requests.post('http://dili_api:5006/insertWrkTimeGen', data=json.dumps(param))

    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def getYryUseDays(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/yryUseDays', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(json.loads(r.text))

    return JsonResponse(ast.literal_eval(r.json()), safe=False)


class diliWebUiSamp(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/diliWebUiSamp.html'



        return render(request, template_name)

class empMgmtRegPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/empMgmtRegPop.html'

        return render(request, template_name)

def empMgmtReg(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/empMgmtRegSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class empMgmtEditPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/empMgmtEditPop.html'

        return render(request, template_name)
        # return render(request, template_name, rr)

def getEditEmpInfo(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/empOneInfo', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def isExistEmpNm(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/isExistEmpNm', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def empMgmtEdit(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])



    r = requests.post('http://dili_api:5006/empMgmtEditSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(datas)

    usr = User.objects.get(username=datas['ipt_empId'])
    usr.password = make_password(datas['ipt_empPw'])
    usr.save()

    return JsonResponse(r.json(), safe=False)

def empMgmtDel(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/empMgmtDelSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class question(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/question.html'

        return render(request, template_name)


class questionDtl(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/questionDtl.html'

        return render(request, template_name)

def getquestionInfo(request):
    param = json.loads(request.GET['param'])

    logger.info("getquestionInfo : dili/views.py")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/questionInfo', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

def getquestionLst(request):
    param = json.loads(request.GET['param'])
    logger.info("getquestionLst : dili/views.py")
    logger.info(param)

    datas = {
        'category': param['category'],
        'searchStr': param['searchStr']
    }

    logger.info(datas)

    # api 호출
    r = requests.get('http://dili_api:5006/question', params=datas)
    paginator = Paginator(r.json(), 10)
    logger.info("----------------")
    logger.info(paginator)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")

    result = paginator.get_page(param['page'])

    logger.info(result)

    data = {
        'list': list(result.object_list),
        'total_records': paginator.count,
        'total_pages': paginator.num_pages,
        'page': result.number,
        'has_next': result.has_next(),
        'has_prev': result.has_previous()
    }

    return JsonResponse(data)

def getQnaPopCnt(request):
    param = json.loads(request.GET['param'])

    logger.info(param)

    params = {
    }

    r = requests.get('http://dili_api:5006/qnaPopCnt', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def getQnaPopUp(request):
    param = json.loads(request.GET['param'])

    logger.info(param)

    params = {
    }

    r = requests.get('http://dili_api:5006/qnaPopUp', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class questionWrPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/questionWrPop.html'

        return render(request, template_name)

def questionWr(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/questionWrSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def questiondetail(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/questiondetail', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json(), safe=False)

class questionEditPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/questionEditPop.html'
        logger.info("questionEditPop Start")
        return render(request, template_name)
    
def questionDelete(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/questionDel', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class questionAnsw(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/questionAnsw.html'

        return render(request, template_name)

def questionAw(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/questionAw', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json(), safe=False)

def qnaAnserReg(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/qnaAnserReg', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class questionUpdateReq(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/questionUpdateReq.html'

        return render(request, template_name)

def qnaUpdate(request):
    logger.info("qnaUpdate Start")
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/qnaUpdate', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def qnaUpdateCnt(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/qnaUpdateCnt', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def qnaSearch(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/qnaSearch', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

#휴게시간 저장
def updateRestTm(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")


    r = requests.post('http://dili_api:5006/updateRestTm', data=json.dumps(param))

    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())
    
def updateDinnRestTm(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")


    r = requests.post('http://dili_api:5006/updateDinnRestTm', data=json.dumps(param))

    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json())

def getPopUpData(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/popUpData', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

class deptMgmt(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/deptMgmt.html'

        return render(request, template_name)

def getDeptInfo(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/deptInfo', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

class deptMgmtRegPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/deptMgmtRegPop.html'

        return render(request, template_name)

def deptMgmtReg(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/deptMgmtRegSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

class deptMgmtEditPop(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/deptMgmtEditPop.html'

        return render(request, template_name)
        # return render(request, template_name, rr)

def deptMgmtReg(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/deptMgmtRegSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

def deptMgmtEdit(request):
    param = json.loads(request.POST['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    datas = {
    }

    for row in param:
        logger.info("------views.py------")
        datas.setdefault(row, param[row])

    r = requests.post('http://dili_api:5006/deptMgmtEditSubmit', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    logger.info(datas)

    return JsonResponse(r.json(), safe=False)

def getEditDeptInfo(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Logging Start")
    logger.info(param)
    logger.info("Parameters Logging End")

    # api 호출
    r = requests.get('http://dili_api:5006/deptOneInfo', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(ast.literal_eval(r.json()), safe=False)

class diliScheduleTotalMgmt(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'dili/diliScheduleTotalMgmt.html'


        # r = requests.get('http://dili_api:5006/hello')
        # rr = {
        #     "result": r.text
        # }
        return render(request, template_name)

def getdiliScheduleTotalMgmt(request):
    param = json.loads(request.GET['param'])

    logger.info("Parameters Start")
    logger.info(param)
    logger.info("Parameters End")

    # api 호출
    r = requests.get('http://dili_api:5006/diliScheduleTotalMgmt', json=param)
    logger.info(r)
    logger.info(r.text)
    logger.info(logger.info(ast.literal_eval(r.json())))
    logger.info(json.loads(r.text))
    return JsonResponse(ast.literal_eval(r.json()), safe=False)