###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class TopSeverity
  constructor: ->
    @hostSelected = ko.observable null
    @hosts = ko.observableArray []

    @severities = 
      '0': ko.observable 0
      '1': ko.observable 0
      '2': ko.observable 0
      '3': ko.observable 0
      '4': ko.observable 0
      '5': ko.observable 0
      '6': ko.observable 0
      '7': ko.observable 0

    @severitySum = ko.computed () =>
      sum = 0
      for severity, value of @severities
        sum += value()
      sum
      
    @query = ko.computed () =>
      cs(
        'query':
          'match_all': {}
        'from': 0
        'size': 0
        'facets':
          'hosts':
            'terms':
              'field': 'host'
          'severities':
            'terms':
              'field': 'severity'
            'facet_filter':
              cs.if @hostSelected, {
                'term':
                  'host': @hostSelected()
              }, {}
        )
      
    ko.computed () =>
      $.ajax
        url: "/_api/query",
        type: 'POST'
        contentType: "application/json"
        data: JSON.stringify @query()()
        dataType: 'json'
        success: (result) =>
          @hosts(host.term for host in result.facets.hosts.terms)
          
          severities = {}
          for severity in result.facets.severities.terms
            severities[severity.term] = severity.count
            
          for severity, value of @severities
            value(severities[severity] or 0)
          
          data = ({'label': Defaults.severity[severity.term], 'value': severity.count } for severity in result.facets.severities.terms)
            
            
          chart_data = [{key: "severity", values: data}]

          chart1 = nv.models.pieChart()
            .x((d) -> d.label)
            .y((d) -> d.value)
            .showLabels(true);
  
          d3.select("#topseverity svg")
            .datum(chart_data)
            .transition().duration(200)
            .call(chart1);

          nv.utils.windowResize(chart1.update)

TopSeverityView =  new TopSeverity
ko.applyBindings TopSeverityView, $('#widget_topseverity').get(0)
