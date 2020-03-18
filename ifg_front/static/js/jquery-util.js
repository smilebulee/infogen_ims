var g_dialog;
var g_modal;
var g_toast;
var g_mask;

$(document).ready(function(){
    g_dialog = new ax5.ui.dialog({
        title: '',
        lang:{
            "ok": "확인", "cancel": "취소"
        }
    });

    g_modal = new ax5.ui.modal({
        onStateChanged: function () {

        }
    });

    g_toast = new ax5.ui.toast({
        containerPosition: "top-right",
        onStateChanged: function(){

        }
    });
	
	g_mask = new ax5.ui.mask();

	$.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });

	$(document).ajaxStart(function(){
		g_mask.open({
			content: '<h1><i class="fa fa-spinner fa-spin"></i> Loading</h1>'
		});
	});

	$(document).ajaxStop(function(){
		g_mask.close();
	});
});

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

(function($){
	$.fn.initGrid = function(opts){
		var options = $.extend({}, $.fn.initGrid.defaultOpts, opts);
		options.target = this;

		var grid = new ax5.ui.grid();
		grid.setConfig(options);

		return grid;
	};
	
	$.fn.initGrid.defaultOpts = {
	    columns: [
	        {key: "a", label: "field  A", align: "center"},
	        {key: "b", label: "field  B", align: "center"},
	        {key: "c", label: "field  C", align: "center"},
	        {key: "d", label: "field  D", align: "center"},
	        {key: "e", label: "field  E", align: "center"}
	    ],
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
			columnHeight: 40
		},
		sortable: false,
		multiSort: false,
		mergeCells: false
	};
})(jQuery);

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
                g_dialog.setConfig({
                    title: 'Error!!'
                });

                g_dialog.alert(jqXHR.statusText);
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

(function($){
	$.ajaxCall = function(data, opts){
	    var ajaxOpts = {
	        method: opts.method,
            url: opts.url,
            data: {param : JSON.stringify(data)},
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown ){
                g_dialog.setConfig({
                    title: 'Error!!'
                });

                g_dialog.alert(jqXHR.statusText);
            },
            success: function(data, textStatus, jqXHR){
                console.log('=====================');
                console.log(data);
                if(typeof opts.callbackFn == 'function') opts.callbackFn(data);
	            else if(typeof opts.callbackFn == 'string') eval(opts.callbackFn + '(data)');
            }
	    }
	    if(opts.global != undefined && typeof opts.global == 'boolean') ajaxOpts.global = opts.global;
	    if(opts.global != undefined && (opts.global == 'true' || opts.global == 'false')) ajaxOpts.global = (opts.global == 'true');

        $.ajax(ajaxOpts);

	};
})(jQuery);