###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'pager', 'vars', 'bootstrap', 'prettyjson'], ($, ko, pager, vars) ->
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
      @hits = ko.observable 0
      
      @loading = ko.observable false
      
      @page = ko.observable 0
      
      @error = ko.observable null
      
      @refreshId = ko.observable setInterval @loadEvents, 5000
      
      @filterMode = ko.observable "fields"
      @freetextValue = ko.observable ""
      @freetextValueFormatted = ko.observable ""

      @filters = 
        'severity': ko.observable ""
        'facility': ko.observable ""
        'host': ko.observable ""
        'program': ko.observable ""
        'message': ko.observable "" 
        
      @filledFilters = ko.computed () =>
        for name, filter of @filters when filter() != ''
          { 'name': name, 'value': filter() }

      @freetext = ko.computed
        read: () =>
        	if @filterMode() == 'fields'
        		f = ''
        		if @filledFilters().length > 0
            	first = 1
            	for filter in @filledFilters()
                if first != 1 
                  f = f + ','
                first = 0
                f = f + '{ "prefix": { "' + filter['name'] + '": "' + filter['value'] + '" } }'
            		console.log f
              
              f = ',
                "filter": {
                  "and": [ ' + f + '
                  ]
                }'
            
            f = '
            {
              "query": { 
                "filtered": {
                  "query": {
                    "match_all" : {}
                  }' + f + '
                }
              },
              "from": ' + @page() * 50 + ',
              "size":  50 ,
              "sort": [{
                "time": {
                  "order": "desc"
                }
              }]
            }'
            
            @freetextValue f
            console.log @freetextValue()
            @freetextValueFormatted pj f
            @loadEvents()

        write: (value) =>
          console.log @freetextValue()	
          @freetextValue value.replace(/<\*>/g, "");



    loadEvents: () =>
      if @filterMode() == 'fields'
        $.ajax
          url: $('#filterform').attr('action')
          type: 'POST'
          contentType: "application/json"
          data: @freetextValue()
          dataType: 'json'
          beforeSend: () => 
            @loading true
          success: (result) =>
            @loading false
            @error null
            @hits result.hits.total
            @events (new EventModel event for event in result.hits.hits)
            #@timeSeries result.facets.histo1.entries
            @addTooltips()
          error: (jqXHR, status, error) =>
            @loading false
            @error error
            @hits 0
            @events []


    setFilter: (name) =>
      (el) => @filters[name] el[name]


    clearFilter: (name) =>
      () => @filters[name] ""


    prevPage: () =>
      if @page() > 0
        @page(@page() - 1)


    nextPage: () =>
      if @page() * 50 + 50 < @hits()
        @page(@page() + 1)

    firstPage: () =>
      @page(0)

    lastPage: () =>
      @page(Math.floor(@hits() / 50))
    
    refreshPage: () =>
    	if @refreshId() == -1
        @refreshId setInterval @loadEvents, 5000	
    	else
        clearInterval @refreshId()
        @refreshId -1


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
        '<h3>#{key}</h3><p>#{y} during #{x}</p>'
          
      d3.select('#timeSeries svg')
        .datum([{ "key": "events", "values": data }])
        .transition().duration(100).call(chart)
  
      nv.utils.windowResize(chart.update)
  
  
    addTooltips: -> 
      $('.tooltip_ip').each (index, element) =>
        el = $(element)
        el.bind 'mouseenter', =>
          
          $.ajax
            url: '/_tooltip/ip'
            type: 'POST'
            data: 'ip=' + el.text()
            dataType: 'json'
            success: (result) =>
              html = '
                <table>
                  <tr><td>IP Address</td><td>' + result.ip + '</td></tr>
                  <tr><td>DNS Name</td><td> ' + result.dns + '</td></tr>
              '
              if result.aliaslist != ""
                html += '<tr><td>Aliases</td><td> ' + result.aliaslist + '</td></tr>'
                
              if result.addresslist != ""
                html += '<tr><td>Addresses</td><td> ' + result.addresslist + '</td></tr>'
                
              html += '
                  <tr><td>Country</td><td>' + result.country + ' <img src="/img/flags/' + result.flagimg + '.gif" title="' + result.country + '" alt="' + result.country + '"/></td></tr>
                </table>
              '
              
              el.attr 'data-toggle', 'tooltip'
              el.attr 'data-original-title', html
              el.tooltip
                content: "dynamic text"
                html: true
                trigger: 'hover'
                container: 'body'
              el.tooltip 'show'


  
  EventListModel
