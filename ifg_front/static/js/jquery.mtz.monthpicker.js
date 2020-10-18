function initDatePickers() {
  // datepicker Korean option
  $.datepicker.regional['ko'] = {
    closeText: '닫기',
    prevText: '이전달',
    nextText: '다음달',
    currentText: '오늘',
    monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
    monthNamesShort: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
    dayNames: ['일', '월', '화', '수', '목', '금', '토'],
    dayNamesShort: ['일', '월', '화', '수', '목', '금', '토'],
    dayNamesMin: ['일', '월', '화', '수', '목', '금', '토'],
    weekHeader: 'Wk',
    dateFormat: 'yy-mm-dd',
    firstDay: 0,
    isRTL: false,
    duration: 200,
    showAnim: 'show',
    showMonthAfterYear: true,
    yearSuffix: '년'
  };

  $.datepicker.setDefaults($.datepicker.regional['ko']);

  $('#schDate').datepicker({
    changeMonth: false,
    changeYear: false,
    defaultDate: $('#schDate').val()
  });

  // monthpicker and year selector start/end year (10 year ago)
  var currentYear = (new Date()).getFullYear();
  var startYear = currentYear - 10;

  var options = {
    startYear: startYear,
    finalYear: currentYear,
    pattern: 'yyyy-mm',
    monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
  };

  $('#schMonth').monthpicker(options);

  // make year selector
  for (var i = currentYear; i >= startYear; i--) {
    if ($("#schYear").attr("pathValue") == i) {
      $("#schYear").append("<option value='" + i + "' selected>" + i + "</option>");
    } else {
      $('#schYear').append("<option value='" + i + "'>" + i + "</option>");
    }
  }
}

$(function() {
  ;
  (function($) {

    var methods = {
      init: function(options) {
        return this.each(function() {
          var
            $this = $(this),
            data = $this.data('monthpicker'),
            year = (options && options.year) ? options.year : (new Date()).getFullYear(),
            settings = $.extend({
              pattern: 'yyyy-mm',
              selectedMonth: null,
              selectedMonthName: '',
              selectedYear: year,
              startYear: year -1,
              finalYear: year + 10,
              monthNames: ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월'],
              id: "monthpicker_" + (Math.random() * Math.random()).toString().replace('.', ''),
              openOnFocus: true,
              disabledMonths: []
            }, options);

          settings.dateSeparator = settings.pattern.replace(/(mmm|mm|m|yyyy|yy|y)/ig, '');

          // If the plugin hasn't been initialized yet for this element
          if (!data) {

            $(this).data('monthpicker', {
              'target': $this,
              'settings': settings
            });

            if (settings.openOnFocus === true) {
              $this.on('focus', function() {
                $this.monthpicker('show');
              });
            }

            $this.monthpicker('parseInputValue', settings);

            $this.monthpicker('mountWidget', settings);

            $this.on('monthpicker-click-month', function(e, month, year) {
              $this.monthpicker('setValue', settings);
              $this.monthpicker('hide');
            });

            // hide widget when user clicks elsewhere on page
            $this.addClass("mtz-monthpicker-widgetcontainer");
            $(document).unbind("mousedown.mtzmonthpicker").on("mousedown.mtzmonthpicker", function(e) {
              if (!e.target.className || e.target.className.toString().indexOf('mtz-monthpicker') < 0) {
                $(this).monthpicker('hideAll');
              }
            });
          }
        });
      },

      show: function() {
        $(this).monthpicker('hideAll');
        var widget = $('#' + this.data('monthpicker').settings.id);
        widget.css("top", this.offset().top + this.outerHeight());
        if ($(window).width() > (widget.width() + this.offset().left)) {
          widget.css("left", this.offset().left);
        } else {
          widget.css("left", this.offset().left - widget.width());
        }
        widget.show();
        widget.find('select').focus();
        this.trigger('monthpicker-show');
      },

      hide: function() {
        var widget = $('#' + this.data('monthpicker').settings.id);
        if (widget.is(':visible')) {
          widget.hide();
          this.trigger('monthpicker-hide');
        }
      },

      hideAll: function() {
        $(".mtz-monthpicker-widgetcontainer").each(function() {
          if (typeof($(this).data("monthpicker")) != "undefined") {
            $(this).monthpicker('hide');
          }
        });
      },

      setValue: function(settings) {
        var
          month = settings.selectedMonth,
          year = settings.selectedYear;

        if (settings.pattern.indexOf('mmm') >= 0) {
          month = settings.selectedMonthName;
        } else if (settings.pattern.indexOf('mm') >= 0 && settings.selectedMonth < 10) {
          month = '0' + settings.selectedMonth;
        }

        if (settings.pattern.indexOf('yyyy') < 0) {
          year = year.toString().substr(2, 2);
        }

        if (settings.pattern.indexOf('y') > settings.pattern.indexOf(settings.dateSeparator)) {
          this.val(month + settings.dateSeparator + year);
        } else {
          this.val(year + settings.dateSeparator + month);
        }

        this.change();
      },

      disableMonths: function(months) {
        var
          settings = this.data('monthpicker').settings,
          container = $('#' + settings.id);

        settings.disabledMonths = months;

        container.find('.mtz-monthpicker-month').each(function() {
          var m = parseInt($(this).data('month'));
          if ($.inArray(m, months) >= 0) {
            $(this).addClass('ui-state-disabled');
          } else {
            $(this).removeClass('ui-state-disabled');
          }
        });
      },

      mountWidget: function(settings) {
        var
          monthpicker = this,
          container = $('<div id="' + settings.id + '" class="ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all" />'),
          header = $('<div class="ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-all mtz-monthpicker" />'),
          combo = $('<select class="mtz-monthpicker mtz-monthpicker-year" />'),
          table = $('<table class="mtz-monthpicker" />'),
          tbody = $('<tbody class="mtz-monthpicker" />'),
          tr = $('<tr class="mtz-monthpicker" />'),
          td = '',
          selectedYear = settings.selectedYear,
          option = null,
          attrSelectedYear = $(this).data('selected-year'),
          attrStartYear = $(this).data('start-year'),
          attrFinalYear = $(this).data('final-year');

        if (attrSelectedYear) {
          settings.selectedYear = attrSelectedYear;
        }

        if (attrStartYear) {
          settings.startYear = attrStartYear;
        }

        if (attrFinalYear) {
          settings.finalYear = attrFinalYear;
        }

        container.css({
          position: 'absolute',
          zIndex: 999999,
          whiteSpace: 'nowrap',
          width: '250px',
          overflow: 'hidden',
          textAlign: 'center',
          display: 'none',
          top: monthpicker.offset().top + monthpicker.outerHeight(),
          left: monthpicker.offset().left
        });

        combo.on('change', function() {
          var months = $(this).parent().parent().find('td[data-month]');
          months.removeClass('ui-state-active');
          if ($(this).val() == settings.selectedYear) {
            months.filter('td[data-month=' + settings.selectedMonth + ']').addClass('ui-state-active');
          }
          monthpicker.trigger('monthpicker-change-year', $(this).val());
        });

        // mount years combo
        for (var i = settings.startYear; i <= settings.finalYear; i++) {
          var option = $('<option class="mtz-monthpicker" />').attr('value', i).append(i);
          if (settings.selectedYear == i) {
            option.attr('selected', 'selected');
          }
          combo.append(option);
        }
        header.append(combo).appendTo(container);

        // mount months table
        for (var i = 1; i <= 12; i++) {
          td = $('<td class="ui-state-default mtz-monthpicker mtz-monthpicker-month" style="padding:5px;cursor:default;" />').attr('data-month', i);
          if (settings.selectedMonth == i) {
            td.addClass('ui-state-active');
          }
          td.append(settings.monthNames[i - 1]);
          tr.append(td).appendTo(tbody);
          if (i % 3 === 0) {
            tr = $('<tr class="mtz-monthpicker" />');
          }
        }

        tbody.find('.mtz-monthpicker-month').on('click', function() {
          var m = parseInt($(this).data('month'));
          if ($.inArray(m, settings.disabledMonths) < 0) {
            settings.selectedYear = $(this).closest('.ui-datepicker').find('.mtz-monthpicker-year').first().val();
            settings.selectedMonth = $(this).data('month');
            settings.selectedMonthName = $(this).text();
            monthpicker.trigger('monthpicker-click-month', $(this).data('month'));
            $(this).closest('table').find('.ui-state-active').removeClass('ui-state-active');
            $(this).addClass('ui-state-active');
          }
        });

        table.append(tbody).appendTo(container);

        container.appendTo('body');
      },

      destroy: function() {
        return this.each(function() {
          $(this).removeClass('mtz-monthpicker-widgetcontainer').unbind('focus').removeData('monthpicker');
        });
      },

      getDate: function() {
        var settings = this.data('monthpicker').settings;
        if (settings.selectedMonth && settings.selectedYear) {
          return new Date(settings.selectedYear, settings.selectedMonth - 1);
        } else {
          return null;
        }
      },

      parseInputValue: function(settings) {
        if (this.val()) {
          if (settings.dateSeparator) {
            var val = this.val().toString().split(settings.dateSeparator);
            if (settings.pattern.indexOf('m') === 0) {
              settings.selectedMonth = val[0];
              settings.selectedYear = val[1];
            } else {
              settings.selectedMonth = val[1];
              settings.selectedYear = val[0];
            }
          }
        }
      }

    };

    $.fn.monthpicker = function(method) {
      if (methods[method]) {
        return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
      } else if (typeof method === 'object' || !method) {
        return methods.init.apply(this, arguments);
      } else {
        $.error('Method ' + method + ' does not exist on jQuery.mtz.monthpicker');
      }
    };

  })(jQuery);

  Date.prototype.yyyymmdd = function() {
    var mm = this.getMonth() + 1; // getMonth() is zero-based
    var dd = this.getDate();

    return [this.getFullYear(),
      (mm > 9 ? '' : '0') + mm,
      (dd > 9 ? '' : '0') + dd
    ].join('-');
  };
  var date = new Date();
  var schDate = date.yyyymmdd();
  $('#schDate').val(schDate);
  $('#schMonth').val(schDate.substr(0, 7));

  initDatePickers();
});
