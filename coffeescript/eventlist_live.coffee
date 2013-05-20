###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class EventModel
  constructor: (data) ->
    @id = data._id
    @time = data._source.time
    @facility = data._source.facility
    @facility_text = ko.computed () ->
      @Defaults.facility[data._source.facility]
    @severity = data._source.severity
    @severity_text = ko.computed () ->
      @Defaults.severity[data._source.severity]
    @detail_url = "/event/" + data._id
    @host = data._source.host
    @program = data._source.program
    @message = data._source.message
    @message_hl = evlist.markIP data._source.message 
    
    
class EventListModel
  constructor: ->
    @events = ko.observableArray []
    @hits = 0
    
    @loading = ko.observable false
    
    @page = ko.observable 0
    
    @error = ko.observable null
    
      
    @query = ko.computed () =>
      "query": 
        "filtered":
          "query":
            "match_all" : {}
      "size": 50
      "sort": [
        "time": 
          "order": "desc"
      ]

  load: =>
    @loadEvents = ko.computed () =>
      $.ajax
        url: '/_api/query'
        type: 'POST'
        contentType: "application/json"
        data: JSON.stringify @query()
        dataType: 'json'
        beforeSend: () => 
          @loading true
        success: (result) =>
          @loading false
          @error null
          @events (new EventModel event for event in result.hits.hits)
        error: (jqXHR, status, error) =>
          @loading false
          @error error
          @events []


  markIP: (msg) ->
    ipv4_regex = /((([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0))/g
    msg.replace(ipv4_regex, '<span class="tooltip_ip">$1</span>');

evlist = new EventListModel
evlist.load()
setInterval evlist.load, 5000

ko.applyBindings evlist
