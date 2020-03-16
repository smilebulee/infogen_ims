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

	$(document).ajaxStart(function(){
		g_mask.open({
			content: '<h1><i class="fa fa-spinner fa-spin"></i> Loading</h1>'
		});
	});

	$(document).ajaxStop(function(){
		g_mask.close();
	});
});

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
	$.ajaxCall = function(url, method, param, callbackFn, global){
	    var data;
	    if(typeof param == 'string') data = param;
	    else data = JSON.stringify(param);

	    var ajaxOpts = {
	        method: method,
            url: url,
            data: data,
            dataType: 'json',
            error: function(jqXHR, textStatus, errorThrown ){
                dialog.setConfig({
                    title: 'Error!!'
                });

                dialog.alert(textStatus);
            },
            success: function(data, textStatus, jqXHR){
                if(typeof callbackFn == 'function') callbackFn;
	            else if(typeof callbackFn == 'string') eval(callbackFn);
            }
	    }
	    if(global != undefined && typeof global == 'boolean') ajaxOpts.global = global;
	    if(global != undefined && (global == 'true' || global == 'false')) ajaxOpts.global = (global == 'true');

        $.ajax(ajaxOpts);

	};
})(jQuery);

(function($){
	$.fn.method = function(opts){
		var options = $.extend({}, $.fn.method.defaultOpts, opts);

		return this.each(function(){
					var $el = $(this);
			   });
	};

	$.fn.method.defaultOpts = {

	};
})(jQuery);