###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class EventModel
    constructor: (data) ->
      @id = data._id
      @timegenerated = data._source.timegenerated
      @timereported = data._source.timereported
      @facility = data._source.facility
      @severity = data._source.severity
      @detail_url = "/event/" + data._id
      @host = data._source.hostname
      @tag = data._source.tag
      @message = data._source.message

class EventListModel
  constructor: ->
    @events = ko.observableArray []
    @loading = ko.observable false
    
  # return a map of filters or the match_all filter if nothing was selected
  getFilters: ->
    result = {}
    $('.filter').each (index, element) =>
      result[$(element).attr('name')] = $(element).val() if $(element).val() != ""
      
    if JSON.stringify(result) is "{}"
      return {"match_all":{}}
    else
      return {"term": result}

  loadEvents: ->
    es_query = 
      "query": evlist.getFilters()
      "facets": 
        "range1" :
          "range":
            "field" : "timereported",
            "ranges" : [
              "from": 2012,
              "to": 2012
            ] 
        "histo1" :
          "date_histogram" :
            "field" : "timereported",
            "interval" : "2h"
    $.ajax
      url: $('#filterform').attr('action')
      type: 'POST'
      contentType: "application/json"
      data: JSON.stringify(es_query)
      dataType: 'json'
      beforeSend: () => 
        @loading true
      success: (result) =>
        @events (new EventModel event for event in result.hits.hits)
        evlist.timeSeries result.facets.histo1.entries
        @loading false
        
  timeSeries: (data) ->
    chart = nv.models.multiBarChart()
      .x((d) -> d.time)
      .y((d) -> d.count)
      
    chart.xAxis
      .tickFormat(d3.format(',f'))
      .rotateLabels(-45)
    chart.yAxis
      .tickFormat(d3.format(',.1f'))
    
    d3.select('#timeSeries svg')
      .datum([{"key": "events", "values": data}])
      .transition().duration(200).call(chart)

    nv.utils.windowResize(chart.update)
    


evlist = new EventListModel
evlist.loadEvents()


# Actions

$('#filterform').bind 'keyup', (event) =>
  evlist.loadEvents()
  
$(".clear-addon").each (index, element) =>
  $(element).bind 'click', (event) =>
    $("#filter_" + $(element).attr("id")).val("")
    evlist.loadEvents()

$("#chartdiv").bind 'plotselected', (event) =>
  evlist.loadEvents()


ko.applyBindings(evlist);  