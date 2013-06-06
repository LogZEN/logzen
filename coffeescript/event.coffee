###
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

class EventModel
  constructor: (data) ->
    @timegenerated = data.timegenerated
    @timereported = data.timereported
    @facility = data.facility
    @severity = data.severity
    @host = data.hostname
    @tag = data.tag
    @message = data.message



class EventView
  constructor: ->
    @event = ko.observable
    @loading = ko.observable false

  loadEvent: ->
    $.ajax
      url: '/_api/get'
      type: 'GET'
      data: 'id=' + $("#event_id").html()
      beforeSend: () => 
        @loading true
      success: (result) =>
        @event (new EventModel result)
        @loading false
        


view = new EventView
view.loadEvent()

ko.applyBindings view