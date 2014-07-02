###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###


define ['jquery', 'knockout', 'ko_mapping', 'vars', 'gridster'], ($, ko, mapping, vars) ->
  ko.bindingHandlers.gridster =
    init: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) =>
      value = ko.utils.unwrapObservable valueAccessor()

      # Build template li element and remove nodes from current element
      template = $('<li>');
      for n in ko.utils.makeArray ko.virtualElements.childNodes element
        template.append ko.cleanNode n

      # Build ul element and make root element gridster compatible
      list = $('<ul style="list-style: none outside none">');
      $(element).append list
      $(element).addClass 'gridster'

      # Create the gridster instance
      gridster = $(list)
        .gridster ko.utils.unwrapObservable value.options
        .data('gridster')

      # Build a mapping from widget list elements to DOM elements
      elements = {}

      # Helper function for adding a gridster widget
      addWidget = (widget) =>
        # Add the widget to gridster using a clone from our template
        e = gridster.add_widget $(template).clone(),
                                ko.utils.unwrapObservable widget.coords?.size_x,
                                ko.utils.unwrapObservable widget.coords?.size_y,
                                ko.utils.unwrapObservable widget.coords?.col,
                                ko.utils.unwrapObservable widget.coords?.row
          .get(0)

        # Remember the created DOM element
        elements[widget] = e

        # Apply bindings to the created elements
        widgetBindingContext = bindingContext.createChildContext ko.utils.unwrapObservable widget
        ko.applyBindingsToDescendants widgetBindingContext, e

      # Helper function for deleting a gridster widget
      deleteWidget = (widget) =>
        # Get the DOM element for this widget
        e = elements[widget]

        # Remove the widget from gridster
        gridster.remove_widget e

        # Remove the entry from the widget mapping
        delete elements[widget]

      # Add all existing widgets
      addWidget widget for widget in ko.utils.unwrapObservable value.widgets

      # Watch the widget list for changes
      value.widgets.subscribe (changes) =>
          for change in changes
            switch change.status
              when 'added' then addWidget change.value
              when 'deleted' then deleteWidget change.value
              else  console.log 'Unhandled change status:', change
        , null, 'arrayChange'

    controlsDescendantBindings: true


  ko.bindingHandlers.require =
    update: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) =>
      value = ko.utils.unwrapObservable valueAccessor()

      require ["#{value}.js",
               "text!#{value}.html"], (vm, html) =>
        ko.utils.setHtml element, html

        if vm?
          childBindingContext = bindingContext.createChildContext vm()
          ko.applyBindingsToDescendants childBindingContext, element

      controlsDescendantBindings: true


  class WidgetModel
    constructor: (r) ->
      @title = ko.observable r.title
      @type = ko.observable r.type

      @coords =
        col: ko.observable r.col
        row: ko.observable r.row
        size_x: ko.observable r.size_x
        size_y: ko.observable r.size_y

      @configuring = ko.observable false

      @viewPath = ko.computed => "/pages/dashboard/widgets/#{@type()}/view"
      @configPath = ko.computed => "/pages/dashboard/widgets/#{@type()}/config"

    configure: () =>
      @configuring true


  class DashboardModel
    constructor: ->
      @widgets = ko.observableArray []

      @gridster = null

      $.ajax
        url: '/_config/dashboard'
        dataType: 'json'
        success: (result) =>
          console.log result

          for r in result
            @widgets.push new WidgetModel r

  DashboardModel
