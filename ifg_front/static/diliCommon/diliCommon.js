/*********************************************************************
*                               Lpad Event
*********************************************************************/
function lpad(s, padLength, padString){
    while(s.length < padLength)
        s = padString + s;
    return s;
}

/*********************************************************************
*                               Rpad Event
*********************************************************************/
function rpad(s, padLength, padString){
    while(s.length < padLength)
        s += padString;
    return s;
}

/*********************************************************************
*   현재 일자를 반환 (YYYY/MM/DD)
*   Input Parameter  - date     [ Date Type  or String Type - YYYY/MM/DD ]
*   Output Parameter - strtDate [ String Type - YYYY/MM/DD ]
*********************************************************************/
function getCurrentDate() {
    var today   = new Date();
    var year    = today.getFullYear();      // 년도
    var month   = today.getMonth();         // 월 (today.getMonth()는 0~11로 출력)
    var date    = today.getDate();          // 날짜
    var day     = today.getDay();           // 요일 (0~6으로 출력, 0:일요일, 1:월요일, 6:토요일)

    var curDate = year+"-"+lpad((month+1).toString(),2,"0")+"-"+lpad(date.toString(),2,"0");

    return curDate
}

/*********************************************************************
*   특정일을 전달받아 해당 일이 속한 주 시작일과 종료일을 Return한다.   (일~월)
*   Input Parameter  - date     [ Date Type  or String Type - YYYY/MM/DD]
*   Output Parameter - baseDate [ String Type - YYYY/MM/DD]
*                      strtDate [ String Type - YYYY/MM/DD]
*                      endDate  [ String Type - YYYY/MM/DD]
*********************************************************************/
function setWeek(date) {

    date = new Date(date);

    baseDate = new Date(date);
    strtDate = date.setDate( date.getDate() - date.getDay() )
    endDate  = date.setDate( date.getDate() + (7 - ( date.getDay() + 1 ) ) )

    var result = {
        "baseDate" : setDateFormat( new Date(baseDate) )
       ,"strtDate" : setDateFormat( new Date(strtDate) )
       ,"endDate"  : setDateFormat( new Date(endDate) )
    };

    return result;
}

/*********************************************************************
*   특정일을 Date Type으로 받아 YYYY/MM/DD 형태의 String 으로 변환한다.
*********************************************************************/
function setDateFormat(date) {

    tgtDate     = new Date(date);
    var year    = tgtDate.getFullYear();      // 년도
    var month   = tgtDate.getMonth();         // 월 (today.getMonth()는 0~11로 출력)
    var date    = tgtDate.getDate();          // 날짜
    var day     = tgtDate.getDay();           // 요일 (0~6으로 출력, 0:일요일, 1:월요일, 6:토요일)

    date = year+"/"+lpad((month+1).toString(),2,"0")+"/"+lpad(date.toString(),2,"0");

    return date
}
/*********************************************************************
*   현재시간 호출
*********************************************************************/
function getCurrentTime() {

    var tgtTime     = new Date();
    var hours    = tgtTime.getHours();      // 시
    var minutes   = tgtTime.getMinutes();         // 분 (today.getMonth()는 0~11로 출력)
    var seconds    = tgtTime.getSeconds();          // 초

    var curTime = lpad(hours.toString(),2,"0")+":"+lpad(minutes.toString(),2,"0")+":"+lpad(seconds.toString(),2,"0");

    return curTime
}

/*********************************************************************
*   전체근무시간 호출
*********************************************************************/
function allWrkTmCall(date, strtTm, endTm, restTm){

    var tmpStrtDate = date+" "+strtTm;
    var tmpEndDate = date+" "+endTm;

    var strtDate = new Date(tmpStrtDate);
    var endDate = new Date(tmpEndDate);

    var tmpSubtractTm = endDate - strtDate;
    //var hour = Math.floor((tmpSubtractTm % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var tmpMinute = tmpSubtractTm/(1000 * 60);

    if(tmpMinute > restTm && tmpMinute > 60){
        tmpMinute -= (restTm + 60)
    }
    //var second = Math.floor((tmpSubtractTm % (1000 * 60)) / 1000);
    var hour = Math.floor(tmpMinute/60);
    var minute = Math.floor(tmpMinute%60);
    var subtractTm = lpad((hour).toString(),2,"0")+":"+lpad((minute).toString(),2,"0")+":00";

    return subtractTm
}

/*********************************************************************
*   초과근무시간 호출
*********************************************************************/
function overWrkTmCall(date, allTmData){
    var overTmChk = "";
    var tmpStrtDate = date+" 08:00:00";
    var tmpEndDate = date+" "+allTmData;
    var strtDate = new Date(tmpStrtDate);
    var endDate = new Date(tmpEndDate);

    if(endDate > strtDate){
        var tmpSubtractTm = endDate - strtDate;
        var hour = Math.floor((tmpSubtractTm % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minute = Math.floor((tmpSubtractTm % (1000 * 60 * 60)) / (1000 * 60));
        var second = Math.floor((tmpSubtractTm % (1000 * 60)) / 1000);
        var subtractTm = lpad((hour).toString(),2,"0")+":"+lpad((minute).toString(),2,"0");
        overTmChk = subtractTm;
    }else {
        overTmChk = "00:00";
    }

    return overTmChk
}

function dateConverting1(date) {

    return date.replace(/\//gi,"-");
}

function dateConverting2(date) {

    return date.replace(/-/gi,"/");
}

function betweenDay(dt) {

    var today = new Date();
    var trgtDay = new Date(today.setDate(today.getDate() - today.getDay()));
    var chk = 0;

    for (var idx = 0;idx <7; idx++) {
        var tmpDate = 0;

        tmpDate = trgtDay;

        if(chk != 0) {
            tmpDate = new Date(trgtDay.setDate(trgtDay.getDate() + 1));
        }

        var tmpYear = tmpDate.getFullYear();
        var tmpMonth = tmpDate.getMonth() + 1;

        if(tmpMonth.toString().length == 1) {
            tmpMonth = "0" + tmpMonth;
        }

        var tmpDay = tmpDate.getDate();

        if(tmpDay.toString().length == 1){
            tmpDay = "0" + tmpDay;
        }

        tmpDate = tmpYear + "-" + tmpMonth + "-" + tmpDay;

        if(tmpDate == dt){
            return true;
        } else {
            chk++;
            continue;
        }


    }

    return false;

}