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
    var year    = today.getFullYear();      // �⵵
    var month   = today.getMonth();         // �� (today.getMonth()�� 0~11�� ���)
    var date    = today.getDate();          // ��¥
    var day     = today.getDay();           // ���� (0~6���� ���, 0:�Ͽ���, 1:������, 6:�����)

    var curDate = year+"/"+lpad((month+1).toString(),2,"0")+"/"+lpad(date.toString(),2,"0");

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
    var year    = tgtDate.getFullYear();      // �⵵
    var month   = tgtDate.getMonth();         // �� (today.getMonth()�� 0~11�� ���)
    var date    = tgtDate.getDate();          // ��¥
    var day     = tgtDate.getDay();           // ���� (0~6���� ���, 0:�Ͽ���, 1:������, 6:�����)

    date = year+"/"+lpad((month+1).toString(),2,"0")+"/"+lpad(date.toString(),2,"0");

    return date
}