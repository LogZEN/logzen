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
      @facilityName = ko.computed () =>
        Defaults.facility[@facility]
      @severity = data._source.severity
      @severityName = ko.computed () =>
        Defaults.severity[@severity]
      @detail_url = "/event/" + data._id
      @host = data._source.hostname
      @program = data._source.program
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
            "interval" : "day"
          
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
        @loading false

  
  plotGraph: (data, tickrange) ->
    plot = $.plot($('#chartdiv'), [data], options = {
      xaxis: {
        ticks: tickrange,
      },
      bars: {
        show: true,
        lineWidth: 1,
        fill: true,
        fillColor: { colors: ["#729fcf", "#3465af"] }
      },
      grid: { 
        hoverable: true, 
        autoHighlight: true 
      },
      tooltip: true,
      tooltipOpts: {
        content: "%y",
        defaultTheme:  false
      },
      colors: ["#204a87"],
      selection: { mode: "x" }
    });

evlist = new EventListModel
evlist.plotGraph([[0,0], [0,0]], [])
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