function submissionCallMap(paramMap, method, url, callBackFunc) {
    $.ajaxCall( paramMap, {
         method : method,
         'url' : url,
         'dataType' : 'json',
         'data' : JSON.stringify(paramMap),
         'async' : false,
         'callbackFn' : function(data){
            // 리턴
            callBackFunc(data);

         }
    });
}

function submissionCallList(paramList, method, url, callBackFunc) {
    $.ajaxCall( paramList, {
         method : method,
         'url' : url,
         'dataType' : 'json',
         'data' : JSON.stringify(paramList),
         'async' : false,
         'callbackFn' : function(data){
            // 리턴
            callBackFunc(data);

         }
    });
}


/* 공통코드 조회 및 select 컴포넌트 option 으로 등록 */
function retrieveCmmCdTest(sbx_id, grp_id)
{
    var param = {
        "sbx_id" : sbx_id,
        "grp_id" : grp_id
    }

     $.ajaxCall( param, {
         method         : 'GET',
         'url'          : '/prj/retrieveCmmCd/',
         'dataType'     : 'json',
         'data'         : JSON.stringify(param),
         'async'        : false,
         'callbackFn'   : function(data){
            for(var i = 0; i < data.length; i++){
                var option = $("<option value = "+data[i].CMM_CD+">"+data[i].CMM_CD_NAME+"</option>");
                $('#'+sbx_id).append(option);
            }
         }
     });
 }


/* 공통코드 조회 및 radio, select 컴포넌트 등록 */
function retrieveCmmCd(cmp_id, grp_id, callBackFunc)
{
    var param = {
        "grp_id" : grp_id
    }

    $.ajaxCall( param, {
        method          : 'GET',
        'url'           : '/dili/retrieveCmmCd/',
        'dataType'      : 'json',
        'data'          : JSON.stringify(param),
        'async'         : false,
        'callbackFn'    : function(data){
            for(var i = 0; i < data.length; i++) {
                if(cmp_id != null && cmp_id != '') {
                    if($('#' + cmp_id).attr('type') == 'radio') {
                        var strRadio ="<label><input type='radio' name='" + data[i].CMM_CD_GRP_ID  + "' value='" + data[i].CMM_CD;

                        if(i == 0) {
                            strRadio += "' checked>&nbsp;" + data[i].CMM_CD_NAME + "&nbsp;&nbsp;&nbsp;</label>";
                        } else {
                            strRadio += "'>&nbsp;" + data[i].CMM_CD_NAME + "&nbsp;&nbsp;&nbsp;</label>";
                        }

                        //var radio = ${strRadio);
                        $('#' + cmp_id).parent().append($(strRadio));

                    } else {
                        var option = $("<option value = "+data[i].CMM_CD+">"+data[i].CMM_CD_NAME+"</option>");
                        $('#' + cmp_id).append(option);
                    }
                }
            }

            if(callBackFunc) {
                if(typeof callBackFunc == 'function') {
                    callBackFunc(data);
                } else if(typeof callBackFunc == 'string') {
                    window[callBackFunc](data);
                }
            }
        }
    });
 }


/* 공통코드 조회 및 checkbox 컴포넌트 등록 */
function retrieveCmmCdChk(cmp_id, grp_id, callBackFunc)
{
    var param = {
        "grp_id" : grp_id
    }

    $.ajaxCall( param, {
        method          : 'GET',
        'url'           : '/dili/retrieveCmmCd/',
        'dataType'      : 'json',
        'data'          : JSON.stringify(param),
        'async'         : false,
        'callbackFn'    : function(data){
            for(var i = 0; i < data.length; i++) {
                if(cmp_id != null && cmp_id != '') {
                    var strChk = ""

                    if(i == 0) {
                        strChk +="<label><input type='checkbox' class='" +"test" + "' name='" + data[i].CMM_CD_GRP_ID + "' id='" + data[i].CMM_CD +"' value='" + data[i].CMM_CD +"' />&nbsp;" + data[i].CMM_CD_NAME + "&nbsp;&nbsp;&nbsp;</label>";

                    } else {
                        strChk +="<label><input type='checkbox' class='" +"test" + "' name='" + data[i].CMM_CD_GRP_ID + "' id='" + data[i].CMM_CD +"' value='" + data[i].CMM_CD +"' />&nbsp;" + data[i].CMM_CD_NAME + "&nbsp;&nbsp;&nbsp;</label>";

                    }

                    //var radio = ${strRadio);
                    $('#' + cmp_id).append($(strChk));

                }
            }

            if(callBackFunc) {
                if(typeof callBackFunc == 'function') {
                    callBackFunc(data);
                } else if(typeof callBackFunc == 'string') {
                    window[callBackFunc](data);
                }
            }
        }
    });
 }


/* 이메일 주소로 사용자 이름 조회 */
function retrieveEmpNmByEmail(empEmail, callBackFunc)
{
    var param = {
        "email" : empEmail
    }

    $.ajaxCall( param, {
        'method'        : 'GET',
        'url'           : '/dili/getEmpName/',
        'dataType'      : 'json',
        'data'          : JSON.stringify(param),
        'async'         : false,
        'callbackFn'    : function(data){
            if(callBackFunc) {
                if(typeof callBackFunc == 'function') {
                    callBackFunc(data);
                } else if(typeof callBackFunc == 'string') {
                    window[callBackFunc](data);
                }
            }
        }
    });
}


/* 이메일 주소로 사용자 부서 조회 */
function retrieveEmpDeptByEmail(empEmail, callBackFunc)
{
    var param = {
        "email" : empEmail
    }

    $.ajaxCall( param, {
        'method'        : 'GET',
        'url'           : '/dili/getEmpDept/',
        'dataType'      : 'json',
        'data'          : JSON.stringify(param),
        'async'         : false,
        'callbackFn'    : function(data){
            //empNm = data[0].EMP_NAME;
            if(callBackFunc) {
                if(typeof callBackFunc == 'function') {
                    callBackFunc(data);
                } else if(typeof callBackFunc == 'string') {
                    window[callBackFunc](data);
                }
            }
        }
    });
}


/* 이메일 주소로 사용자 부서 사업부장 정보 조회 */
function retrieveEmpDeptGmByEmail(empEmail, callBackFunc) {

    var param = {
        "email" : empEmail
    }

    $.ajaxCall( param, {
        'method'        : 'GET',
        'url'           : '/dili/getEmpDeptGm/',
        'dataType'      : 'json',
        'data'          : JSON.stringify(param),
        'async'         : false,
        'callbackFn'    : function(data){
            //empNm = data[0].EMP_NAME;
            if(callBackFunc) {
                if(typeof callBackFunc == 'function') {
                    callBackFunc(data);
                } else if(typeof callBackFunc == 'string') {
                    window[callBackFunc](data);
                }
            }
        }
    });
}

/* 이메일 주소로 사용자 부서 현장대리인 정보 조회 */
function retrieveEmpDeptPrByEmail(empEmail, callBackFunc) {

    var param = {
        "email" : empEmail
    }

    $.ajaxCall( param, {
        'method'        : 'GET',
        'url'           : '/dili/getEmpDeptPr/',
        'dataType'      : 'json',
        'data'          : JSON.stringify(param),
        'async'         : false,
        'callbackFn'    : function(data){
            //empNm = data[0].EMP_NAME;
            if(callBackFunc) {
                if(typeof callBackFunc == 'function') {
                    callBackFunc(data);
                } else if(typeof callBackFunc == 'string') {
                    window[callBackFunc](data);
                }
            }
        }
    });
}

/* 이메일 주소로 사용자 권한 보유 여부 확인 */
function checkEmpAuthByEmail(userId, authCd) {
    var authIds = sessionStorage.getItem("authId");
    var authArr = authIds.split('|');
    if(authArr.indexOf(authCd) > -1) {
        return true;
    }
    return false;
}

/* 이메일 주소, 권한코드 배열로 사용자 권한 보유 여부 확인 및 변수 생성
ex.
checkEmpAuthsByEmail("asete93", ["USER", "ADMIN", "TEST"]);
으로 호출하여 사용할 경우,
isUser, isAdmin, isTest 변수 생성 및 그 안에 권한 보유 여부 true, false 로 담김
*/
function checkEmpAuthsByEmail(userId, authCdArr) {
    var authIds = sessionStorage.getItem("authId");
    var authArr = authIds.split('|');

    for(auth of authCdArr)
    {
        var strTmp = "is" + auth.substring(0, 1).toUpperCase() + auth.substring(1).toLowerCase() + " = ";
        if(authArr.indexOf(auth) > -1) {
            strTmp += "true;";
        } else {
            strTmp += "false;";
        }
        eval(strTmp);
    }
}

/* input, textArea 글자수 체크 함수
제한 글자 수 초과 시 alert 창 띄운 뒤 넘어간 만큼 잘라낸 후 focus */
function chkLength(obj, maxByte) {
    var strValue = obj.value;
    var strLen = strValue.length;
    var totalByte = 0;
    var len = 0;
    var oneChar = "";
    var str2 = "";
    for (var i = 0; i < strLen; i++) {
        oneChar = strValue.charAt(i);
        if (escape(oneChar).length > 4) {
            totalByte += 2;
        }
        else {
            totalByte++;
        }
        // 입력한 문자 길이보다 넘치면 잘라내기 위해
        if (totalByte <= maxByte) {
            len = i + 1;
        }
    }
    // 넘어가는 글자는 자른다.
    if (totalByte > maxByte) {
        alertMsg(maxByte + "자를 초과 입력 할 수 없습니다.", function() {
            $("#" + obj.id).focus();
            str2 = strValue.substr(0, len);
            obj.value = str2;
            //chkLength(obj, 4000);
        });
        return;
    }
}

/* 자리수만큼 0 채우기 (근무 시간 형식 지정) */
function fillZero(width, str){
    str = str + '';
    return str.length >= width ? str:new Array(width-str.length+1).join('0')+str;
    //남는 길이만큼 0으로 채움
}


/* 시간 차이 구하기 (근무 시간) */
function getTimeDiff(fromDtm, toDtm, isNormalWrk) {
    var dt1         = new Date(fromDtm);
    var dt2         = new Date(toDtm);
    isNormalWrk     = isNormalWrk == null ? true : isNormalWrk;

    var tDiff = dt2 - dt1; //밀리초 단위 시간차 반환

    var hh = Math.floor((tDiff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var mi = Math.floor((tDiff % (1000 * 60 * 60)) / (1000 * 60));
    var ss = Math.floor((tDiff % (1000 * 60)) / 1000);

    //시간 차 9시간 이상인 경우, 식사 시간 1시간 제외
    if(isNormalWrk == true && hh >= 9) {
        hh = hh - 1;
    }

    return fillZero(2, hh) + fillZero(2, mi) + fillZero(2, ss);
}


/* url로 넘긴 param 받기
사용방법 : var value = $.urlParam("key"); //url 에서 get 으로 넘긴 parameter 'key' 받기
*/
$.urlParam = function(name){
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);

    if (results == null || results == '' ){
        console.log("method=get::param= { " + name + " : null }");
        return null;

    } else{
        console.log("method=get::param= { " + name + " : " + results[1] + " }");
        return results[1] || 0;

    }
}


/* Dialog Setting */
var cf_dialog = new ax5.ui.dialog();
var nTitle =  "<span style='color:#fd7e14;font-size:20px;'><i class='fa fa-check-circle'></i></span> CHECK";

cf_dialog.setConfig({
    title: nTitle,
    theme : "info",
    lang:{
        "ok": "확인",
        "cancel": "취소"
    }
});


