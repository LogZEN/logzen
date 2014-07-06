###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

require.config
  baseUrl: '/'
  paths:
    jquery:'libs/jquery/dist/jquery'
    knockout:'libs/knockoutjs/dist/knockout.debug'
    pager:'libs/pagerjs/dist/pager.min'
    bootstrap:'libs/bootstrap/dist/js/bootstrap'
    text: 'libs/requirejs-text/text'
    gridster: 'libs/gridster/dist/jquery.gridster'
    humanize: 'libs/jquery.humanize'
  shim:
    'bootstrap':
      deps: [ 'jquery' ]
    'humanize':
      deps: [ 'jquery' ]
    'gridster':
      deps: [ 'jquery' ]
    'ko_mapping':
      deps: [ 'knockout' ]

@requireVM = (module) ->
  (callback) ->
    require ["/pages/#{module}.js"], (vm) ->
      callback new vm


@requireHTML = (module) ->
  (page, callback) ->
    require ["text!/pages/#{module}.html"], (html) ->
      $(page.element).html html
      callback()


require ['jquery', 'knockout', 'pager', 'utils', 'bootstrap'], \
        ($, ko, pager, utils) ->
  class Main extends utils.LoadingModel
    constructor: ->
      pager.extendWithPage @
      pager.onBindingError.add (event) ->
        console.error event.error

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
            callback()
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
        success: (result) ->
          window.location.href = "/";


    # check whether initial configuration has been done
    checkInitialConf: ->
      $.ajax
        url: '/_config'
        type: 'GET'
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




  main = new Main

  ko.applyBindings main
  
  main.checkInitialConf()

  
  pager.start()
