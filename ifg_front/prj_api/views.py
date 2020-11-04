from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.helpers import ajax_login_required
# Create your views here.
from django.views import View
from django.views import generic
from django.http import JsonResponse
from django.core.paginator import Paginator
import requests
import logging
import json

logger = logging.getLogger(__name__)


class Prj_api_index(generic.TemplateView):
    def get(self, request, *args, **kwargs):
        template_name = 'prj/index.html'

        r = requests.get('http://prj_api:5002/hello')
        rr = {
            "result": r.text
        }

        return render(request, template_name, rr)


# 프로젝트 목록 조회 화면 호출
def prjListSrch(request):
    template_name = 'prj/prjListSrch.html'

    return render(request, template_name)

# 개발자 등록 화면
def devReg(request):
    template_name = 'prj/devReg.html'

    return render(request, template_name)


@login_required
def retrieve(request):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    params = {}  # get 일때 사용
    data = {
        'username': 'bulee',
        'email': 'bulee@infogen.co.kr'
    }

    # requests.get(url, params=params)
    res = requests.post('http://prj_api:5002/retrieve', headers=headers,
                        json=data)  # data가 다층 구조일 땐 json.dumps(data) 사용

    if res.status_code == requests.codes.ok:
        retVal = res.json()
        retVal['status'] = 'ok'
    else:
        retVal = {
            'status': 'fail'
        }
    logger.debug(retVal);
    return JsonResponse(retVal)


@login_required
def prjReg(request):
    template_name = 'prj/prjReg.html'

    return render(request, template_name)


# 프로젝트 정보 조회
def retrievePrjInfo(request):
    param = json.loads(request.GET['param'])

    params = {
        'prj_cd': param['prj_cd'],
    }

    r = requests.get('http://prj_api:5002/retrievePrjInfo', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


# 프로젝트 요구 스킬 조회
def retrieveReqSkil(request):
    param = json.loads(request.GET['param'])

    params = {
        'prj_cd': param['prj_cd'],
    }

    r = requests.get('http://prj_api:5002/retrieveReqSkil', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


# 프로젝트 등록 스킬명 조회
def retrieveSkilName(request):
    param = json.loads(request.GET['param'])

    params = {

    }

    r = requests.get('http://prj_api:5002/retrieveSkilName', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


# 프로젝트 저장
@ajax_login_required
def prjSave(request):
    userId = str(request.user)
    param = json.loads(request.POST['param'])

    datas = {
        'userId': userId
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://prj_api:5002/prjSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)


# 프로젝트 삭제
@ajax_login_required
def prjDelete(request):
    param = json.loads(request.POST['param'])

    datas = {
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://prj_api:5002/prjDelete', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json())


# 프로젝트별투입현황관리 프로젝트 상세정보
def retrievePrjDetlInfo(request):
    param = json.loads(request.GET['param'])
    logger.info(param)
    logger.info("프로젝트별투입현황관리 프로젝트 상세정보")
    params = {
        'prjCd': param['prjCd']
    }
    r = requests.get('http://prj_api:5002/retrievePrjDetlInfo', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())
    return JsonResponse(r.json(), safe=False)


# 프로젝트별투입현황관리 화면
def prjInpuMgmt(request):
    template_name = 'prj/prjInpuMgmt.html'

    return render(request, template_name)


# 프로젝트별투입현황관리 조회
def prjInpuSearch(request):
    param = json.loads(request.GET['param'])
    logger.info("prjInpuSearch : skil/views.py")
    datas = {
        'prjCd': param['prjCd']
    }
    r = requests.get('http://prj_api:5002/prjInpuSearch', params=datas)
    return JsonResponse(r.json(), safe=False)


# 프로젝트별투입현황관리 삭제
def prjInpuDelete(request):
    param = json.loads(request.POST['param'])
    logger.info(param)
    logger.info("prjInpuDelete : skil/views.py")
    datas = {
        'prjCd': param['PRJ_CD'],
        'empNo': param['EMP_NO'],
    }

    logger.info('request.post : ' + request.POST['param'])

    r = requests.post('http://prj_api:5002/prjInpuDelete', data=datas)
    return JsonResponse(r.json(), safe=False)


# 프로젝트별투입현황관리 저장
def prjInpuSave(request):
    param = json.loads(request.POST['param'])
    userId = str(request.user)
    logger.info(param)
    for data in param:
        if '__created__' in data and data['__created__']:
            logger.info("__created__")
            datas = {
                'empNo': data['EMP_NO'],
                'prjCd': data['PRJ_CD'],
                'slinGrd': data['SLIN_GRD'],
                'inpuStrtDay': data['INPU_STRT_DAY'],
                'inpuEndDay': data['INPU_END_DAY'],
                'cntcStrtDay': data['CNTC_STRT_DAY'],
                'cntcEndDay': data['CNTC_END_DAY'],
                'crgeJob': data['CRGE_JOB'],
                'rmks': data['RMKS'],
                'state': 'created',
                'userId' : userId
            }
        else:
            logger.info("modified")
            datas = {
                'empNo': data['EMP_NO'],
                'prjCd': data['PRJ_CD'],
                'slinGrd': data['SLIN_GRD'],
                'inpuStrtDay': data['INPU_STRT_DAY'],
                'inpuEndDay': data['INPU_END_DAY'],
                'cntcStrtDay': data['CNTC_STRT_DAY'],
                'cntcEndDay': data['CNTC_END_DAY'],
                'crgeJob': data['CRGE_JOB'],
                'rmks': data['RMKS'],
                'state': 'modified',
                'userId': userId
            }
        r = requests.post('http://prj_api:5002/prjInpuSave', data=datas)
    return JsonResponse(r.json())


# 프로젝트 목록 조회
def prjListSearch(request):
    logger.info("prjListSearch : prj/views.py")
    param = json.loads(request.GET['param'])
    logger.info(param)

    datas = {
        'deptDiv': param['deptDiv'],
        'skilDiv': param['skilDiv']
    }

    logger.info(datas)
    r = requests.get('http://prj_api:5002/prjListSearch', params=datas)

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

#부서 코드 조회
def getDeptCd(request):
    param = json.loads(request.GET['param'])
    logger.info('===============================')
    logger.info(param)
    logger.info('===============================')
    datas = {}

    r = requests.get('http://prj_api:5002/getDeptCd', params=datas)

    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))

    return JsonResponse(r.json(), safe=False)

# 개발자 정보 조회
def retrieveDevInfo(request):
    param = json.loads(request.GET['param'])
    logger.info(param)

    params = {
        'emp_no': param['emp_no'],
    }

    r = requests.get('http://prj_api:5002/retrieveDevInfo', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

# 개발자 정보 저장
def devSave(request):
    userId = str(request.user)
    param = json.loads(request.POST['param'])

    datas = {
        'userId': userId
    }

    for row in param:
        datas.setdefault(row, param[row])
    logger.info(datas)
    r = requests.post('http://prj_api:5002/devSave', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

# 개발자 정보 삭제
def devDelete(request):
    param = json.loads(request.POST['param'])

    datas = {
    }

    for row in param:
        datas.setdefault(row, param[row])

    r = requests.post('http://prj_api:5002/devDelete', data=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json())

#공통 코드 조회
def retrieveCmmCd(request):
    param = json.loads(request.GET['param'])
    logger.info('param')
    logger.info(param)

    params = {
        'grp_id': param['grp_id'],
    }

    r = requests.get('http://prj_api:5002/retrieveCmmCd', params=params)
    logger.info(r)
    logger.info(r.text)
    logger.info(r.json())

    return JsonResponse(r.json(), safe=False)

# 개발자 정보 조회
def devMgmt(request):
    template_name = 'prj/devMgmt.html'

    return render(request, template_name)

def devMgmtSearch(request):

    param = json.loads(request.GET['param'])
    logger.info("devMgmtSearch : prj/views.py")
    datas = {
        'devpBlco': param['devpBlco'],
        'empName': param['empName'],
        'devpDivsCd': param['devpDivsCd']
    }

    logger.info(datas)
    r = requests.get('http://prj_api:5002/devMgmtSearch', params=datas)
    logger.info(r)
    logger.info(r.text)
    logger.info("----------------")
    logger.info(r.json())
    logger.info(json.loads(r.text))
    # return JsonResponse(r.json())
    return JsonResponse(r.json(), safe=False)