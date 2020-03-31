/**********************************************
jquery-uti.js
공통 jquery util
history
    - 2020.03 이병욱 최초작성
***********************************************/

var g_dialog;       // 다이얼로그 공통
var g_modal;        // 모달 공통
var g_toast;        // 토스트 팝업 공통
var g_mask;         // 로딩 마스크 공통

/********************************************
페이지 로딩 후 공통 적용
********************************************/
$(document).ready(function(){
    // 공통 다이얼로그 생성, alert이나 confirm팝업
    g_dialog = new ax5.ui.dialog({
        title: '',
        lang:{
            "ok": "확인", "cancel": "취소"
        }
    });

    // 공통 모달 팝업 생성
    g_modal = new ax5.ui.modal({
        onStateChanged: function () {

        }
    });

    // 공통 토스트 팝업생성
    g_toast = new ax5.ui.toast({
        containerPosition: "top-right",
        onStateChanged: function(){

        }
    });

	// 공통 로딩 마스크 생성
	g_mask = new ax5.ui.mask();

    // ajax csrftoken 설정
	$.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

    // ajax 요정 시작시 로딩 마스크 실행
	$(document).ajaxStart(function(){
		g_mask.open({
			content: '<h1><i class="fa fa-spinner fa-spin"></i> Loading</h1>'
		});
	});

    // ajax 종료시 로딩 마스크 close
	$(document).ajaxStop(function(){
		g_mask.close();
	});
});

/**********************************************8
쿠키 가져오기
************************************************/
function getCookie(c_name){
    if (document.cookie.length > 0){
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1){
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }

/*********************************************************
그리드 공통
그리드 생성 후 그리드 객체 반환
ex) $('divID').initGrid(json type grid option);
**********************************************************/
(function($){
	$.fn.initGrid = function(opts){
        var defaultOptions = {
            showLineNumber: true,
            showRowSelector: false,
            multipleSelect: false,
            lineNumberColumnWidth: 40,
            rowSelectorColumnWidth: 27,
            frozenColumnIndex: 0,
            frozenRowIndex: 0,
            header: {
                align: "center",
                columnHeight: 40
            },
            body: {
                align: "center",
                columnHeight: 40,
                onClick : function(){

                }
            },
            sortable: false,
            multiSort: false,
            mergeCells: false,
            page: {
                display: false,
                statusDisplay: false
            },
            columnMinWidth : 100
        };

		//var options = $.extend(true, $.fn.initGrid.defaultOpts, opts);
		var options = $.extend(true, defaultOptions, opts);
		options.target = this;

		var grid = new ax5.ui.grid();
		grid.setConfig(options);
        $(this, '[data-ax5grid-panel="header"]').find('td').addClass('font-weight-bolder');

		return grid;
	};
	
	$.fn.initGrid.defaultOpts = {
		showLineNumber: true,
		showRowSelector: false,
        multipleSelect: false,
        lineNumberColumnWidth: 40,
        rowSelectorColumnWidth: 27,
		frozenColumnIndex: 0,
        frozenRowIndex: 0,
		header: {
			align: "center",
			columnHeight: 40
        },
        body: {
			align: "center",
			columnHeight: 40,
			onClick : function(){

            }
		},
		sortable: false,
		multiSort: false,
		mergeCells: false,
		page: {
		    display: false,
            statusDisplay: false
		},
		columnMinWidth : 100
	};
})(jQuery);

/*********************************************************
ajax 공통
특정 div나 form 등 특정 태그 내의 input, select box, textarea의 값들을 json 데이터로 변환하여 ajax 요청
ex) $('divID or formID or etcID...').ajaxCall(json type jquery ajax option);
opts : json. url, method, callback
**********************************************************/
(function($){
	$.fn.ajaxCall = function(opts){
	    var data = {};

	    $(this).find('input,select,textarea').each(function(idx){
            var key = $(this).attr('name');
            var val = $(this).val();
            var type = $(this).attr('type');

            if(val != ''){
                if(type == 'checkbox'){
                    if($(this).is(':checked')){
                        if(data.hasOwnProperty(key)){
                            data[key].push(val);
                        }else{
                            var arr = new Array();
                            arr.push(val);

                            data[key] = arr;
                        }
                    }
                }else{
                    data[key] = val;
                }
            }else{
                data[key] = '';
            }
	    });

	    var ajaxOpts = {
	        method: opts.method,
            url: opts.url,
            data: {param : JSON.stringify(data)},
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown ){
                alertMsg(jqXHR.statusText);
            },
            success: function(data, textStatus, jqXHR){
                if(typeof opts.callbackFn == 'function') opts.callbackFn(data);
	            else if(typeof opts.callbackFn == 'string') eval(opts.callbackFn + '(data)');
            }
	    }
	    if(opts.global != undefined && typeof opts.global == 'boolean') ajaxOpts.global = opts.global;
	    if(opts.global != undefined && (opts.global == 'true' || opts.global == 'false')) ajaxOpts.global = (opts.global == 'true');

        $.ajax(ajaxOpts);
	};
})(jQuery);

/*********************************************************
ajax 공통
개발자가 직접 생성한 데이터로 ajax 호출
ex) $.ajaxCall(json type data, json type jquery ajax option);
data : 서버로 전송할 데이터. json or array
opts : json. url, method, callback
**********************************************************/
(function($){
	$.ajaxCall = function(data, opts){
	    var ajaxOpts = {
	        method: opts.method,
            url: opts.url,
            data: {param : JSON.stringify(data)},
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown ){
//                g_dialog.setConfig({
//                    title: 'Error!!'
//                });

                if(jqXHR.status == '403'){
                    alertMsg('세션이 종료 되었습니다.<br/>로그인 페이지로 이동합니다.', function(){
                        location.href = '/main/login/';
                    });
                }else{
                    alertMsg(jqXHR.statusText);
                }

            },
            success: function(data, textStatus, jqXHR){
                if(typeof opts.callbackFn == 'function') opts.callbackFn(data);
	            else if(typeof opts.callbackFn == 'string') eval(opts.callbackFn + '(data)');
            }
	    }
	    if(opts.global != undefined && typeof opts.global == 'boolean') ajaxOpts.global = opts.global;
	    if(opts.global != undefined && (opts.global == 'true' || opts.global == 'false')) ajaxOpts.global = (opts.global == 'true');

        $.ajax(ajaxOpts);

	};
})(jQuery);

/*********************************************************
alert
commnet : 메세지. string
**********************************************************/
function alertMsg(comment, callbackFn){
    var title = '<span style="color:#c82333;font-size:20px;"><i class="fa fa-exclamation-circle"></i></span> ALERT';
    //var msg = '<div class="row">'
    //msg += '<div class="col-3"><span style="color:#c82333"><i class="fa fa-exclamation-circle fa-5x"></i></span></div>';
    //msg += '<div class="col-9">' + comment + '</div>';
    //msg += '</div>';

    g_dialog.alert({
        theme : 'info',
        title : title,
        msg : comment
    }, callbackFn);
}

/*********************************************************
confirm
comment : 메세지. string
callbackFn : 확인 클릭시 실행할 함수
**********************************************************/
function confirmMsg(comment, callbackfn){
    var title = '<span style="color:#fd7e14;font-size:20px;"><i class="fa fa-check-circle"></i></span> CHECK';
    //var msg = '<div class="row">'
    //msg += '<div class="col-3"><span style="color:#fd7e14"><i class="fa fa-check-circle fa-5x"></i></span></div>';
    //msg += '<div class="col-9">' + comment + '</div>';
    //msg += '</div>';

    g_dialog.confirm({
        theme : 'info',
        title : title,
        msg : comment
    }, function(){
        if(typeof callbackfn == 'function') callbackfn();
        else if(typeof callbackfn == 'string') eval(callbackfn + '()');
    });
}

/*********************************************************
공통코드 조회
grpArr : 코드 그룹 배열 ex) ['SAMPLE_01', 'SAMPLE_02']
callbackFn : 공통코드 조회 후 실행할 함수
**********************************************************/
function getCodes(grpArr, callbackFn){
    var data = {
        grps : grpArr
    };
    var options = {
        method : 'get',
        url : "/cmm/getCodes",
        //global : false,
        callbackFn :  callbackFn
    };

    $.ajaxCall(data, options);
}

/*********************************************************
공통코드 조회하여 select box, check box, radio 생성
ex) $(selector).makeForm();
selector로 선택한 element에는 cd-grp 라는 attribute가 존재해야 함..
select box의 경우는 select 태그내에 option 태그만 생성
check box와 radio의 경우는 div 태그내에 생성되어야 하므로 div에 cd-type(checkbox or radio)이라는 attribute가 필수
**********************************************************/
(function($){
    $.fn.makeForm = function(){
        var grpArr = new Array();
        var selArr = new Array();
        $(this).each(function(){
            var grp = $(this).attr('cd-grp');
            if(grp != undefined && grp != ''){
                grpArr.push(grp);
                selArr.push(this);
            }
        });

        grpArr = grpArr.reduce(function(a, b){
            if(a.indexOf(b) < 0) a.push(b);
            return a;
        }, []);     // 중복제거

        getCodes(grpArr, function(data){
            if($.isEmptyObject(data)) return false;
            $.each(grpArr, function(idx, val){
                if(data.hasOwnProperty(val) && data[val].length > 0){
                    var codes = data[val];
                    $('[cd-grp="' + val + '"]').each(function(){
                        if(this.nodeName == 'SELECT'){
                            var options = '<option value="">선택</option>';

                            $.each(codes, function(i, code){
                                options += '<option value="' + code.cmm_cd + '">' + code.cmm_nm + '</option>';
                            });

                            $(this).html(options);
                        }else{
                            var type = $(this).attr('cd-type');
                            var name = $(this).attr('cd_name');
                            var html = '';

                            if(name == undefined || name == '') name = codes[0].grp_cd;

                            switch(type){
                                case 'checkbox':
                                    $.each(codes, function(i, code){
                                        var id = code.grp_cd + code.cmm_cd;
                                        html += '<input class="form-check-input" type="checkbox" id="' + id + '" name="' + name + '" value="' + code.cmm_cd + '">';
                                        html += '<label class="form-check-label" for="' + id + '" style="margin-left:20px;margin-right:20px;">' + code.cmm_nm + '</label>';
                                    });

                                    break;
                                case 'radio':
                                     $.each(codes, function(i, code){
                                        var id = code.grp_cd + code.cmm_cd;
                                        html += '<input class="form-check-input" type="radio" name="exampleRadios" id="' + id + '" value="' + code.cmm_cd + '" >'
                                        html += '<label class="form-check-label" for="' + id + '" style="margin-left:20px;margin-right:20px;">' + code.cmm_nm + '</label>';
                                     });
                                    break;
                            }
                            $(this).html(html);
                        }
                    });
                }
            });
        });
    };
})(jQuery);

/*********************************************************
페이징 생성
ex) $('#divId').makePagingNavi(obj, goPageFn);
obj : 페이징 정보 json. 현재페이지, 전체페이지수, 이전페이지 존재여부, 다음페이지 존재여부
goPageFn : 페이지 조회 스크립트 함수명. string
**********************************************************/
(function($){
    $.fn.makePagingNavi = function(obj, goPageFn){
        if(obj.page == undefined || isNaN(Number(obj.page))) return;
        if(obj.total_pages == undefined || isNaN(Number(obj.total_pages))) return;
        if(obj.has_prev == undefined || typeof obj.has_prev != 'boolean') return;
        if(obj.has_next == undefined || typeof obj.has_next != 'boolean') return;
        if(goPageFn == undefined || typeof goPageFn != 'string') return;

        var cPage = obj.page;       // 현재페이지
        var tPage = obj.total_pages;        // 전체페이지
        var hasP = obj.has_prev;
        var hasN = obj.has_next;
        var pDisable = '';
        var nDisable = '';
        var cDisable = '';
        var html = '';

        html += '<nav aria-label="Page navigation" style="margin-top: 10px;">';
        html += '	<ul class="pagination pagination-sm justify-content-center">';
        if(!hasP) pDisable = ' disabled';
        html += '		<li class="page-item' + pDisable + '">';
        html += '			<a class="page-link" href="javascript:' + goPageFn + '(' + (cPage - 1) + ')" aria-label="Previous">';
        html += '				<span aria-hidden="true">&laquo;</span>';
        html += '			</a>';
        html += '		</li>';

        var start = 0;
        var end = 0;

        if(tPage <= 5){
            start = 1;
            end = tPage;
        }else{
            start = cPage - 2;
            end = cPage + 2;

            if(start < 1){
                start = 1;
                end = 5;
            }

            if(end > tPage){
                start = tPage - 4;
                end = tPage;
            }
        }
        for(var i = start;i <= end;i++){
            if(i == cPage) {
                html += '       <li class="page-item active" aria-current="page">';
                html += '           <span class="page-link">' + i + '<span class="sr-only">(current)</span></span>';
                html += '       </li>';
            }else{
                html += '		<li class="page-item"><a class="page-link" href="javascript:' + goPageFn + '(' + i + ')">' + i + '</a></li>';
            }
        }
        if(!hasN) nDisable = ' disabled';
        html += '		<li class="page-item' + nDisable + '">';
        html += '			<a class="page-link" href="javascript:' + goPageFn + '(' + (cPage + 1) + ')" aria-label="Next">';
        html += '				<span aria-hidden="true">&raquo;</span>';
        html += '			</a>';
        html += '		</li>';
        html += '	</ul>';
        html += '</nav>';

        $(this).html(html);
    };
})(jQuery);