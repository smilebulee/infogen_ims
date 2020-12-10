function submissionCallMap(paramMap, method, url, callBackFunc) {
    $.ajaxCall( paramMap, {
         method : method,
         'url' : url,
         'dataType' : 'json',
         'data' : JSON.stringify(paramMap),
         'async' : false,
         'callbackFn' : function(data){
            callBackFunc(data);

         }
    });
}

function submissionCallList(paramList, method, url) {
    $.ajaxCall( paramList, {
         method : method,
         'url' : url,
         'dataType' : 'json',
         'data' : JSON.stringify(paramList),
         'async' : false,
         'callbackFn' : function(data){

            // 리턴
            g_toast.push('저장 되었습니다.');
            $('#exitSchdModal').click();
         }
    });
}