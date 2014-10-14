###
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['knockout', 'utils'], \
       (ko, utils) ->
  # Syslog severity names.
  #
  # The name index to string mapping according to RFC 3164.
  severity = [
    "emerge",
    "alert",
    "critical",
    "error",
    "warning",
    "notice",
    "info",
    "debug"
  ]

  # Syslog facility names.
  #
  # The name index to string mapping according to RFC 3164.
  facility = [
    "kern",
    "user",
    "mail",
    "daemons",
    "auth",
    "syslog",
    "lpr",
    "news",
    "uucp",
    "cron",
    "security",
    "ftp",
    "ntp",
    "logaudit",
    "logalert",
    "clock",
    "local0",
    "local1",
    "local2",
    "local3",
    "local4",
    "local5",
    "local6",
    "local7"
  ]

  # The model used for an event received from the API.
  #
  # The event class maps an event received from the API and extends the model
  # using some helping properties.
  class EventModel
    ipv4_regex = ///
      (([1-9][0-9]{0,2})|0)\.
      (([1-9][0-9]{0,2})|0)\.
      (([1-9][0-9]{0,2})|0)\.
      (([1-9][0-9]{0,2})|0)
    ///g

    constructor: (data) ->
      @id = data._id

      @time = data._source.time

      @facility = data._source.facility
      @facility_text = facility[@facility]

      @severity = data._source.severity
      @severity_text = severity[@severity]

      @host = data._source.host
      @program = data._source.program

      @message = data._source.message
      @message_hl = @highlite data._source.message

    highlite: (msg) ->
      msg.replace ipv4_regex, '<span class="tooltip_ip">$1</span>'


  # A base class for sending queries to the API.
  #
  # A elasticsearch query is send to the API and the result is received. The
  # 'query' observable is watched to build the request against the API and
  # executed every time the observable changes.
  class QueryModel extends utils.IntervalRequestingModel
    constructor: () ->
      @request = ko.computed () => [
              '/_api/query'
              method: 'POST'
              contentType: 'application/json'
              dataType: 'json'
              data: ko.toJSON @query
            ]

      super()


  # A base class for event lists received from the API.
  #
  # The event list is requested from the API and updated after the 'filter'
  # observable has changed or after an optional timeout specified in the
  # 'interval' observable. The result of the request is transformed into a list
  # of 'EventModel' instances and stored in the 'events' array observable. In
  # addition to that, the overal hit count is stored in the 'hits' observable.
  #
  # The whole result of the request is stored in the 'result' observable as
  # returned by the API.
  class EventListModel extends QueryModel
    constructor: () ->
      @events = ko.observableArray []
      @hits = ko.observable 0

      super()

    done: (result) ->
      @hits result.hits.total
      @events (new EventModel event for event in result.hits.hits)

    fail: () ->
      @events []
      @hits 0


  return {
    severity: severity
    facility: facility
    EventModel: EventModel
    QueryModel: QueryModel
    EventListModel: EventListModel
  }
