###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'model'], \
       ($, ko, model) ->
  class TabModel extends model.EventListModel
    constructor: (id = null) ->
      @id = id ? "#{Math.round Math.random() * Math.pow 2, 16}"

      @title = ko.observable 'New Tab'

      # Pagination submodel
      @page =
        current: ko.observable 0
        size: ko.observable 50

      # Filters for the common message fields
      @filters =
        severity: ko.observable ''
        facility: ko.observable ''
        host: ko.observable ''
        program: ko.observable ''
        message: ko.observable ''

      # The query as required by the base model
      @query = {}
#      ko.computed () =>
#        filter:
#          bool:
#            must: for name, filter of @filters when filter() != ''
#              term: (
#                term = {}
#                term[name] = filter()
#                term
#              )
#        from: @page.current() * @page.size()
#        size: @page.size()
#        sort:
#          time:
#            order: 'desc'

      super()

      # Extend the pagination submodel with a page count after initializing the
      # base as the computed depends on it
      @page.count = ko.computed () => @hits() // @page.size()
      @page.next  = () => @page.current Math.min(@page.current() + 1,
                                                 @page.count())
      @page.prev  = () => @page.current Math.max(@page.current() - 1,
                                                 0)
      @page.first = () => @page.current 0
      @page.last  = () => @page.current @page.count()
      @page.crop  = () => @page.current Math.min(@page.count(),
                                                 Math.min(@page.current(), 0))


    # Ensure the current page is in bound after updating.
    done: (result) ->
      super(result)
      # Ensure the current page is in bound after updating
      @page.crop()


    # Ensure the current page is in bound after updating.
    fail: (error) ->
      super(error)
      @page.crop()


    # A monade returning a function to set a filter.
    #
    # The returned function accepts a string value and updates the filter
    # observable with the passed name.
    setFilter: (name) ->
      (el) => @filters[name] el[name]


    # A monade returning a function to clear a filter.
    #
    # The returned function clears the filter observable with the passed name.
    clearFilter: (name) ->
      () => @filters[name] ''


  class PageModel
    constructor: () ->
      @tabs = ko.observableArray [
        new TabModel()
      ]

    add: () =>
      @tabs.push new TabModel()

    remove: (tab) =>
      @tabs.remove tab

