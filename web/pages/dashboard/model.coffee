###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'pager', 'vars', 'bootstrap'], ($, ko, pager, vars) ->
  class DashboardModel
    constructor: ->
      @loading = ko.observable false
      
      $.ajax
        url: '/_config/widget'
        dataType: 'json'
        success: (result) =>
          @loadWidgets result


    loadWidgets: (conf) ->
      all = 0
      html = ""
      for column in conf
        all += column.size
        html += '<div class="span' + column.size + '" id="col' + column.id + '"></div>'
      
      if all == 12
        $('#widgetcolumns').append(html)
        for column in conf
          row = 0
          for w in column.widget
            row += 1
            $('#col' + column.id).append($("<div id='widget_" + w + column.id + row + "'>").load('/pages/widget/' + w + '/view.html'))
            ko.applyBindings requireVM('widget/' + w) $("#widget_" + w + column.id + row)
      
      else
        $('#widgetNumberError').modal('show')


  DashboardModel