###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

require.config 
  urlArgs: 'v=' + new Date()
  baseUrl: '/js'
  paths:
    jquery:'libs/jquery-2.0.3'
    knockout:'libs/knockout-2.3.0'
    ko_mapping: 'libs/knockout.mapping'
    pager:'libs/pager-1.0.1.min'
    bootstrap:'libs/bootstrap'
    vars: 'vars'
    text: 'libs/text'
    prettyjson: 'libs/pretty_json'
    humanize: 'libs/jquery.humanize'
    gridster: 'libs/jquery.gridster'
  shim:
    'bootstrap':
      deps: [ 'jquery' ]
    'humanize':
      deps: [ 'jquery' ]
    'quickflip':
      deps: [ 'jquery' ]
    'gridster':
      deps: [ 'jquery' ]
    'ko_mapping':
      deps: [ 'knockout' ]

@requireVM = (module) ->
  (callback) ->
    require ["/pages/#{module}/model.js"], (vm) ->
      callback new vm


@requireHTML = (module) ->
  (page, callback) ->
    require ["text!/pages/#{module}/view.html"], (html) ->
      $(page.element).html html
      callback()


require ['jquery', 'knockout', 'pager', 'bootstrap', 'prettyjson', 'gridster'], ($, ko, pager) ->
	class VM
    constructor: ->
      @loading = ko.observable false
      
      @configured = ko.observable false
      
      @ui_displayMainMenu = ko.computed =>
        @configured() == true and @username() != ""
        
      @username = ko.observable ""
      
      @evlists = ko.observableArray [
        id: +(new Date())
        title: ko.observable 'Eventlist'
      ]
      

    # check whether the current user is logged in or not
    # redirect to login page, if not logged in
    isLoggedIn: (page, route, callback) =>
      $.ajax
        url: '/_auth/getlogin'
        dataType: 'json'
        success: (result) =>
          if result.success == true
            @username result.username
            callback();
          else
            window.location.href = "/#system/login";
        error: (jqXHR, status, error) =>
          @error error
          window.location.href = "/#system/login";


    # logout
    logout: ->
      $.ajax
        url: '/_auth/logout'
        dataType: 'json'
        success: (result) =>
          window.location.href = "/";


    # check whether initial configuration has been done
    checkInitialConf: ->
      $.ajax
        url: '/_config/get'
        type: 'POST'
        data: 'key=configured'
        dataType: 'json'
        success: (result) =>
          @configured result.value.toLowerCase() == "true"

      
    # add a new tab to the eventlist page
    remove_evlist: (evlist) =>
    	@evlists.remove evlist


    # remove a tab from the eventlist page
    add_evlist: () =>
    	@evlists.push 
    		id: +(new Date())
    		title: ko.observable 'New Tab'




  vm = new VM
  pager.extendWithPage vm
  ko.applyBindings vm
  
  vm.checkInitialConf()
  
  pager.onBindingError.add( 
  	(event) ->
      console.log event               # DEBUG
      page = event.page
      $(page.element).empty().append('<div class="alert"> Error Loading Page</div>')
  )
  
  pager.start()
  