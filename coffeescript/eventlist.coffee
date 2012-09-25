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
    
  hideLoadingIcon: ->
    $("#loading").hide()
  
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
            "ranges" : [
              "from": 2012,
              "to": 2012
            ] 
        "histo1" :
          "date_histogram" :
            "field" : "timereported",
            "interval" : "day"
          
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
    evlist.hideLoadingIcon()
    console.log(JSON.stringify(result))
    
    rows = ""
    if result.hits.hits.length
      for i in [0 .. result.hits.hits.length - 1]
        object = result.hits.hits[_i];
        console.log(object)
        rows += '
          <tr> 
            <td class="column_menu">
              <ul class="nav hover-nav" style="display:inline-block">
                <li class="dropdown">
                  <a class="dropdown-toggle" href="#"><i class="icon-chevron-down"></i></a>
                  <ul class="dropdown-menu">
                    <li><a href="/event/' + object['_id'] + '"><i class="icon-info-sign"></i> Display details</a></li>
                    <li><a href="{{searchengine}}' + encodeURIComponent(object._source['message']) + '"><i class="icon-globe"></i> Search with {{searchengine_name}}</a></li>
                  </ul>
                </li>
              </ul>
              <i class="icon-eye-open event_tooltip" title="' + object['_id'] + '"></i>
            </td>
            <td colspan="2" class="event">' + object._source['timereported'] + '</td>
            <td colspan="2" class="event">
              <span class="badge color_' + object._source['severity'] + '" id="' + object._source['id'] + '">
                <a href="javascript:void(0)" onclick="$(\'#filter_severity\').val($(this).html()); updateAction();">' + object._source['severity'] + '</a>
              </span>
            </td>
            <td colspan="2" class="event">
              <a href="javascript:void(0)" onclick="$(\'#filter_facility\').val($(this).html()); updateAction();">' + object._source['facility'] + '</a>
            </td>
            <td colspan="2" class="event">
              <a href="javascript:void(0)" onclick="$(\'#filter_host\').val($(this).html()); updateAction();">' + object._source['fromhost'] + '</a>
            </td>
            <td colspan="2" class="event">
              <a href="javascript:void(0)" onclick="$(\'#filter_program\').val($(this).html()); updateAction();"></a>
            </td>
            <td colspan="2">
              <a href="javascript:void(0)" onclick="$(\'#filter_message\').val(\'' + object._source['message'] + '\'); updateAction();">' + addIpTooltipTags(object._source['message']) + '</a>
            </td>
          </tr>
        '
    else
      rows = '<tr><td colspan="13" id="noresults">No events found</td></tr>'

    $('tbody').empty().append(rows);
    
  
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

console.log (defaults.severity[0])

# Actions

$('#filterform').bind 'keyup', (event) =>
  evlist.loadEvents()
  
$(".clear-addon").each (index, element) =>
  $(element).bind 'click', (event) =>
    $("#filter_" + $(element).attr("id")).val("")
    evlist.loadEvents()

$("#chartdiv").bind 'plotselected', (event) =>
  evlist.loadEvents()
  