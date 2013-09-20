###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class TopHosts
  constructor: ->
    @rangeSelected = ko.observable 1
    @rangeSelectedLabel = ko.computed () =>
      switch @rangeSelected()
        when 1 then 'last day'
        when 7 then 'last week'
        when 30 then 'last month'
        when 365 then 'last year' 

    @qry = ko.computed () =>
      now = new Date()
      from = new Date(now.getFullYear(), now.getMonth(), now.getDate() - @rangeSelected(), 
        now.getHours(), now.getMinutes(), now.getSeconds(), 0)
      
      'query':
        'match_all': {}
      'from': 0
      'size': 0
      'facets':
        'byhost':
          'terms':
            'field': 'host'
          'facet_filter':
            'range':
              'time' :
                 'from': from
                 'to': now


  updateRange: (range) =>
    @rangeSelected range
    TopHostsView.load()


  load: ->
    $.ajax
      url: '/_api/query'
      dataType: 'json'
      type: 'POST'
      contentType: 'application/json'
      data: JSON.stringify @qry()
      success: (result) =>
        if result.facets.byhost.terms.length
          data = ({label: next['term'], value: next['count']} for next in result.facets.byhost.terms)
        else
          data = [{label: 0, value: 0}]
          
        chart_data = [{key: 'events', values: data}]

        chart1 = nv.models.pieChart()
          .x((d) -> d.label)
          .y((d) -> d.value)
          .showLabels(true);

        d3.select('#events_by_host svg')
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


TopHostsView = new TopHosts
TopHostsView.load()

ko.applyBindings TopHostsView, $('#widget_tophosts').get(0)
