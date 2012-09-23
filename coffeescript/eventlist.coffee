###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###


class Eventlist
  constructor: ->
    timerange = []
  
  displayLoadingIcon: ->
    $("#loading").show()
  
  # return the map of filters or all if nothing was selected
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
          "range" :
            "field" : "timereported",
            "ranges" :
              "from": "2012",
              "to": "2012" 
    
    $.ajax({
      url: $('#filterform').attr('action'),
      type: 'POST',
      contentType: "application/json",
      data: JSON.stringify(es_query),
      dataType: 'json',
      success: evlist.handleResult,
      beforeSend: evlist.displayLoadingIcon
    })
    
  handleResult: (result) ->
    console.log(JSON.stringify(result))
  
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

evlist = new Eventlist 
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
  