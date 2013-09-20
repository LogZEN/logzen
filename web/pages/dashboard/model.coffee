###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###


define ['jquery', 'knockout', 'ko_mapping', 'pager', 'vars', 'bootstrap'], ($, ko, mapping, pager, vars) ->
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
    	@widgetModels = ko.observableArray []
    	
    	@layout = mapping.fromJS []
      	
    	$.ajax
        url: '/_config/dashboard/layout'
        dataType: 'json'
        success: (result) =>
        	console.log result
        	
        	mapping.fromJS result, @layout 
        	 
        	
        	#for id, config of result
        	#	require ["/pages/widget/#{config.type}/model.js", "text!/pages/widget/#{config.type}/view.html"], (vm, html) =>
        	#	  vm = new vm()
        	#	  @widgetModels.push ({ id: id, vm: vm, html: html })

  
  	    



  DashboardModel