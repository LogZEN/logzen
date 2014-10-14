###
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['knockout', 'jquery'], \
       (ko, $) ->
  # A helper base class for models providing loading and error support.
  #
  # The class provides a 'loading' observable indicating the current state and
  # an 'error' observable containing an occured error, if any. To set the
  # loading flag, the 'loader' method can be called which returns a jQuery
  # 'deferred' object which will handle completion by clearing the 'loading'
  # observable. If the returned deferred does not complete successfully, the
  # 'loading' flag is reset and the 'error' observable is updated with the
  # passed error message.
  #
  # To wrap AJAX request in a loading block, the 'ajax' method can be used in
  # the same way the jQuery 'ajax' method can be used.
  LoadingModel: class LoadingModel
    constructor: () ->
      @loading = ko.observable false
      @error = ko.observable null

    loader: () ->
      $.Deferred () =>
        @error null
        @loading true
      .done () =>
        @error null
        @loading false
      .fail (error) =>
        @error error
        @loading false

    ajax: (url, settings) ->
      s = @loader()

      $.ajax url, settings
      .done (result) -> s.resolve result
      .fail (_, status, error) -> s.reject error

      return s.promise()


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
      [url, settings] = ko.unwrap @request
      @ajax url, settings
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

