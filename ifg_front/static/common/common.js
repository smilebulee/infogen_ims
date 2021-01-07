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
function retrieveCmmCd(sbx_id, grp_id){
    var param = {
        "sbx_id" : sbx_id,
        "grp_id" : grp_id
    }

     $.ajaxCall( param, {
             method : 'GET',
             'url' : '/prj/retrieveCmmCd/',
             'dataType' : 'json',
             'data' : JSON.stringify(param),
             'async' : false,
             'callbackFn' : function(data){
                for(var i = 0; i < data.length; i++){
                    var option = $("<option value = "+data[i].CMM_CD+">"+data[i].CMM_CD_NAME+"</option>");
                    $('#'+sbx_id).append(option);
                }
             }
     });
 }