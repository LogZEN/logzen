###
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'api'], \
       ($, ko, api) ->
  # A helper base class for models providing loading and error support.
  #
  # The class provides a 'loading' observable indicating the current state and
  # an 'error' observable containing an occured error, if any.
  #
  # To wrap AJAX request in a loading block, the 'ajax' method can be used. It
  # takes a request executor function which executes the request call. The
  # function is called with the API instance used to do the request and must
  # return the result of that API call.
  LoadingModel: class LoadingModel
    constructor: () ->
      @loading = ko.observable false
      @error = ko.observable null


    ajax: (request) ->
      @error null
      @loading true

      request(api)
      .done (result) =>
        @error null
        @loading false
      .fail (_, status, error) =>
        @error error
        @loading false



  # A helper base class for models doing simple AJAX requests.
  #
  # The 'execute' method can be used to trigger an AJAX request build using the
  # 'request' observable (containing a tuple of url and settings).
  #
  # In addition, if the 'request' observables is changed, the request is
  # triggered automatically (using a rate limitation waiting for the changes to
  # settle). The result of the AJAX request is stored in the 'result' observable
  # and is passed to the 'done' function if such a function exists. Errors will
  # clean the 'result' observable and will trigger the 'fail' function if such a
  # function exists.
  #
  # TODO: Instead of calling the done / fail function, some kind of deferred
  # chaining should be used.
  RequestingModel: class RequestingModel extends LoadingModel
    constructor: () ->
      super()

      # Container for the received result
      @result = ko.observable null

      # Subscribe to the url and the data observable and trigger the request
      @request.extend
        method: 'notifyWhenChangesStop'
        timeout: 400
      .subscribe () => @execute()

      @execute()

    execute: () ->
      # Get the request executor
      request = ko.unwrap @request

      @ajax request
      .fail (_, status, error) =>
        @result null
        if @fail?
          @fail error
      .done (result) =>
        @result result
        if @done?
          @done result


  # A helper base class for models doing automatic reloading AJAX requests.
  #
  # An interval timer triggering requests is controlled by the interval
  # observable. If the interval observable is set to an positive integer, the
  # value is interpreted as a refresh rate in milliseconds. A negative, zero or
  # null value disables the timer.
  IntervalRequestingModel: class IntervalRequestingModel extends RequestingModel
    constructor: (interval = null) ->
      super()

      timer = null

      @interval = ko.observable interval
      @interval.subscribe (interval) ->
        if @interval?
          clearInterval timer

        if interval? and interval > 0
          timer = setTimer @request, interval

