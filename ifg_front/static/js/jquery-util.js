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
	$.fn.method = function(opts){
		var options = $.extend({}, $.fn.method.defaultOpts, opts);
		
		return this.each(function(){
					var $el = $(this);
			   });
	};
	
	$.fn.method.defaultOpts = {
	
	};
})(jQuery);