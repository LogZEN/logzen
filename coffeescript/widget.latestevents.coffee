###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class EventModel
  constructor: (data) ->
    @time = $.humanize("datetime", data._source.time)
    @facility = data._source.facility
    @severity = data._source.severity
    @host = data._source.host
    @program = data._source.program
    @message = data._source.message
    
class LatestEvents
  constructor: ->
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
    
    @query = ko.computed () =>
      "query":
        "match_all": {}
      "from": 0
      "size": 20
      "filter":
        "and": [
          "range":
            "severity":
              "from": 0
              "to": @severitySelected()
        ]
      "sort": [
        "time":
          "order": 
            "desc"
      ]

  update: (severity) =>
    @severitySelected severity
    view.load()
    
  load: =>
    $.ajax
      url: "/_api/query",
      type: 'POST'
      contentType: "application/json"
      data: JSON.stringify @query()
      dataType: 'json'
      success: (result) =>
        @events (new EventModel event for event in result.hits.hits)


LatestEventsView = new LatestEvents
LatestEventsView.load()

setInterval LatestEventsView.load, 5000

ko.applyBindings LatestEventsView, $('#widget_latestevents').get(0)
