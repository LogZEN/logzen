###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###


define ['jquery', 'knockout', 'pager', 'vars', 'bootstrap'], ($, ko, pager, vars) ->
  class EventModel
    constructor: (data) ->
      @count = data.count
      @message = data.term
  
  
  class TopEvents
    constructor: ->
      @excludeMessages = ko.observableArray []
      @events = ko.observableArray []
      
      @severitySelected = ko.observable 7
      @severitySelectedLabel = ko.computed () =>
        switch @severitySelected()
          when 1 then "Alert and above"
          when 2 then "Critical and above"
          when 3 then "Error and above"
          when 4 then "Warning and above"
          when 5 then "Notice and above"
          when 6 then "Info and above"
          else "All severities"
      
      @rangeSelected = ko.observable 1
      @rangeSelectedLabel = ko.computed () =>
        switch @rangeSelected()
          when 1 then 'in last day'
          when 7 then 'in last week'
          when 30 then 'in last month'
          when 365 then 'in last year' 
          
      @query = ko.computed () =>
        now = new Date()
        from = new Date(now.getFullYear(), now.getMonth(), now.getDate() - @rangeSelected(), 
          now.getHours(), now.getMinutes(), now.getSeconds(), 0)
          
        "query":
          "match_all": {}
        "size": 0
        'facets':
          'byevent':
            'terms':
              'field': 'message'
              "size": 5
              'exclude' : @excludeMessages()
            'facet_filter':
              'and': [
                {
                'range':
                  'severity':
                    'from': 0
                    'to': @severitySelected()
                }
                {
                'range':
                  'time' :
                     'from': from
                     'to': now
                }
              ]
  
  
    updateSeverity: (severity) =>
      @severitySelected severity
      TopEventsView.load()
  
  
    updateRange: (range) =>
      @rangeSelected range
      TopEventsView.load()
  
  
    exclude: (m) =>
      @excludeMessages.push m
      TopEventsView.load()
  
  
    include: (m) =>
      @excludeMessages.splice(@excludeMessages.indexOf(m), 1)
      TopEventsView.load()
  
  
    load: =>
      $.ajax
        url: "/_api/query",
        type: 'POST'
        contentType: "application/json"
        data: JSON.stringify @query()
        dataType: 'json'
        success: (result) =>
          @events (new EventModel event for event in result.facets.byevent.terms)
          add_qtips()
  
  
  TopEvents
