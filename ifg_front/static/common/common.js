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
function retrieveCmmCdTest(sbx_id, grp_id){
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

/* 공통코드 조회 및 radio, select 컴포넌트 등록 */
function retrieveCmmCd(cmp_id, grp_id){
    var param = {
        "cmp_id" : cmp_id,
        "grp_id" : grp_id
    }

    $.ajaxCall( param, {
        method : 'GET',
            'url' : '/dili/retrieveCmmCd/',
            'dataType' : 'json',
            'data' : JSON.stringify(param),
            'async' : false,
            'callbackFn' : function(data){
                for(var i = 0; i < data.length; i++){
                    if($('#' + cmp_id).attr('type') == 'radio') {
                        var radio = $("<label><input type='radio' name='"+data[i].CMM_CD_GRP_ID+"' value='"+data[i].CMM_CD+"'>"+data[i].CMM_CD_NAME+"&nbsp;&nbsp;</label>");
                        console.log(radio);

                        $('#' + cmp_id).parent().append(radio);

                        //윤상은 작업중 2020-01-07
                    } else {
                        var option = $("<option value = "+data[i].CMM_CD+">"+data[i].CMM_CD_NAME+"</option>");
                        $('#' + cmp_id).append(option);
                    }
                }
            }
    });
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

