###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class TopHosts
  constructor: ->
    @qry = 
      "query":
        "match_all": {}
      "from": 0
      "size": 0
      "sort": []
      "facets":
        "byhost":
          "terms":
            "field": 
              "hostname"

  load: ->
    $.ajax
      url: "/_api/query"
      dataType: 'json'
      type: 'POST'
      contentType: "application/json"
      data: JSON.stringify @qry
      success: (result) =>
        data = ({label: next['term'], value: next['count']} for next in result.facets.byhost.terms)
        chart_data = [{key: "events", values: data}]

        chart1 = nv.models.pieChart()
          .x((d) -> d.label)
          .y((d) -> d.value)
          .showLabels(true);

        d3.select("#events_by_host svg")
          .datum(chart_data)
          .transition().duration(200)
          .call(chart1);

        chart2 = nv.models.discreteBarChart()
          .x((d) -> d.label)
          .y((d) -> d.value)
          .staggerLabels(true)

        d3.select('#top_hosts svg')
          .datum(chart_data)
          .transition().duration(200)
          .call(chart2)

        nv.utils.windowResize(chart1.update)
        nv.utils.windowResize(chart2.update)

view = new TopHosts
view.load()
ko.applyBindings view