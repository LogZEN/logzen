###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'events', 'bootstrap', 'prettyjson'], ($, ko, events) ->
  class Model extends events.EventListModel
    constructor: ->
      @page =
        current: ko.observable 0
        size: ko.observable 50

      @filters =
        severity: ko.observable ''
        facility: ko.observable ''
        host: ko.observable ''
        program: ko.observable ''
        message: ko.observable ''

      @query = ko.computed () =>
        filter:
          bool:
            must: for name, filter of @filters when filter() != ''
              term: (
                term = {}
                term[name] = filter()
                term
              )
        from: @page.current() * @page.size()
        size: @page.size()
        sort:
          time:
            order: 'desc'

      super()

      # Extend the page submodel with a page count after initializing the base as the computed depends on it
      @page.count = ko.computed () => @hits() // @page.size()
      @page.next  = () => @page.current Math.min(@page.current() + 1, @page.count())
      @page.prev  = () => @page.current Math.max(@page.current() - 1, 0)
      @page.first = () => @page.current 0
      @page.last  = () => @page.current @page.count()
      @page.crop  = () => @page.current Math.max(0, Math.min(@page.current(), @page.count()))

    done: () ->
      super()
      # Ensure the current page is in bound after updating
      @page.crop()

    fail: () ->
      super()
      # Ensure the current page is in bound after updating
      @page.crop()

    ### A monade returning a function to set a filter.
    #
    # The returned function accepts a string value and updates the filter observable with the passed name.
    ###
    setFilter: (name) ->
      (el) => @filters[name] el[name]

    ### A monade returning a function to clear a filter.
    #
    # The returned function clears the filter observable with the passed name.
    ###
    clearFilter: (name) ->
      () => @filters[name] ''

    ### Move to next page
    #
    # Does nothing if the current page is already the last one.
    ###
    pageNext: () ->
      if @page.current() < @page.count()
        @page.current @page.current() + 1

    ### Move to previous page
    #
    # Does nothing if the current page is already the first one.
    ###
    pagePrev: () ->
      if @page.current() > 0
        @page.current @page.current() - 1

    ### Move to first page
    ###
    pageFirst: () ->
      @page.current 0

    ### Move to last page
    ###
    pageLast: () ->
      @page.current @page.count()

    ### Ensures the current page is in bounds.
    #
    # Updates the curent page it is not between 0 and the page count. The current page value is ensured to be in borders
    # by moving to the next closest page.
    ###
    pageSanetize: () ->
      @page.current Math.max(0, Math.min(@page.current(), @page.count()))

