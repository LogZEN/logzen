###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###


define ['jquery', 'knockout', 'ko_mapping', 'pager', 'vars', 'bootstrap', 'gridster'], ($, ko, mapping, pager, vars) ->
  ko.bindingHandlers.widget =
		init: (element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) =>
			value = ko.utils.unwrapObservable valueAccessor()
			
			ko.utils.setHtml element, value.html
			
			childBindingContext = bindingContext.createChildContext value.vm 
			console.log childBindingContext
			ko.applyBindingsToDescendants childBindingContext, element
			
			controlsDescendantBindings: true

	
  class DashboardModel
    constructor: ->
      @widgetModels = []

      #@layout = mapping.fromJS []
      @layout = ko.observableArray []

      g = $(".gridster ul").gridster(
        widget_margins: [10, 10]
        widget_base_dimensions: [160, 160])
        .data('gridster')

      $.ajax
        url: '/_config/dashboard/layout'
        dataType: 'json'
        success: (result) =>
          #@layout result
          #console.log @layout()

          for r in result
            $.ajax
              url: "/_config/dashboard/config?name=#{r.wid}"
              dataType: 'json'
              success: (result) =>
                console.log result

                require ["/pages/widget/#{result.type}/model.js", "text!/pages/widget/#{result.type}/view.html"], (vm, html) =>
                  console.log r.wid
                  vm = new vm()

                  @layout.push
                    id: r.wid
                    layout: r
                    vm: vm
                    html: html

                  @widgetModels[r.wid] =
                    vm: vm
                    html: html

                  g.add_widget('<li class="new" data-bind="template: {name: \'template_widget\', data: \'' + r.wid + '\'}"></li>', 2, 1);




  DashboardModel