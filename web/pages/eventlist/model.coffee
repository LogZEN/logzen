###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'pager', 'vars', 'bootstrap'], ($, ko, pager, vars) ->
	pivot = (key, value, data) ->
    result = {}
    result[data[key]] = data[value]
    
    return result


  class EventModel
    constructor: (data) ->
      @id = data._id
      @time = data._source.time
      @facility = data._source.facility
      @facility_text = ko.computed () ->
        vars.facility[data._source.facility]
      @severity = data._source.severity
      @severity_text = ko.computed () ->
        vars.severity[data._source.severity]
      @detail_url = "/event/" + data._id
      @host = data._source.host
      @program = data._source.program
      @message = data._source.message
      @message_hl = @markIP data._source.message 
      
    markIP: (msg) ->
      ipv4_regex = /((([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0))/g
      msg.replace(ipv4_regex, '<span class="tooltip_ip">$1</span>');


  class EventListModel
    constructor: ->
      @events = ko.observableArray []
      @hits = 0
      
      @loading = ko.observable false
      
      @page = ko.observable 0
      
      @error = ko.observable null
      
      @filterMode = ko.observable "fields"
      
      @freetextValue = ko.observable ""
      @freetext = ko.computed 
        read: () =>
        	if @filterMode() == 'fields' or (@filterMode() == 'freetext' and @freetextValue() != '')
        		"test"
        	else if @filterMode() == 'freetext'
        		@freetextValue()
        		
        write: (value) =>
        	@freetextValue(value)
        
      @filters = 
        'severity': ko.observable ""
        'facility': ko.observable ""
        'host': ko.observable ""
        'program': ko.observable ""
        'message': ko.observable "" 
        
      @filledFilters = ko.computed () =>
        for name, filter of @filters when filter() != ""
          {'name': name, 'value': filter() }
        
      @query = ko.computed () =>
        "query": 
          "filtered":
            "query":
              "match_all" : {}
        "facets":
          "histo1":
            "date_histogram":
              "field": "time"
              "interval": "day"
        "from": @page() * 50
        "size": 50
        "sort": [
          "time": 
            "order": "desc"
        ]
  
      @loadEvents = ko.computed () =>
        $('#tab1 a').click (e) =>
          e.preventDefault()
          @tab('show')
          
        $.ajax
          url: $('#filterform').attr('action')
          type: 'POST'
          contentType: "application/json"
          data: JSON.stringify @query()
          dataType: 'json'
          beforeSend: () => 
            @loading true
          success: (result) =>
            @loading false
            @error null
            @hits = result.hits.total
            @events (new EventModel event for event in result.hits.hits)
            #@timeSeries result.facets.histo1.entries
            @addTooltips()
          error: (jqXHR, status, error) =>
            @loading false
            @error error
            @hits = 0
            @events []


    setFilter: (name) =>
      (el) => @filters[name] el[name]


    clearFilter: (name) =>
      () => @filters[name] ""


    prevPage: () =>
      if @page() > 0
        @page(@page() - 1)


    nextPage: () =>
      if @page() * 50 + 50 < @hits
        @page(@page() + 1)


    timeSeries: (data) ->
      chart = nv.models.multiBarTimeSeriesChart()
        .x((d) -> d.time)
        .y((d) -> d.count)
        
      chart.xAxis
        .tickFormat((d) -> d3.time.format('%x') new Date(d))
        .rotateLabels(-45)
        
      chart.yAxis
        .tickFormat(d3.format(',.0f'))
        
      chart.tooltip = (key, x, y, e, graph) ->
        "<h3>#{key}</h3><p>#{y} during #{x}</p>"
          
      d3.select('#timeSeries svg')
        .datum([{"key": "events", "values": data}])
        .transition().duration(100).call(chart)
  
      nv.utils.windowResize(chart.update)
  
  
    addTooltips: -> 
      $('.tooltip_ip').each (index, element) =>
        el = $(element)
        el.bind 'mouseenter', =>
          $.ajax
            url: '/tooltips/ip'
            data: 
              ip: el.text()
            success: (d) ->
              el.attr 'data-toggle', 'tooltip'
              el.attr 'data-original-title', d
              el.tooltip
                content: "dynamic text"
                html: true
                trigger: 'click'
                container: 'body'
              el.tooltip 'show'


  EventListModel
