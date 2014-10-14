###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

require.config
  urlArgs: 'v=' + new Date()
  baseUrl: '/'
  paths:
    jquery:'libs/jquery/dist/jquery'
    knockout:'libs/knockoutjs/dist/knockout.debug'
    pager:'libs/pagerjs/pager'
    bootstrap:'libs/bootstrap/dist/js/bootstrap'
    text: 'libs/requirejs-text/text'
    gridster: 'libs/gridster/dist/jquery.gridster'
    humanize: 'libs/jquery.humanize'
    fermata: 'libs/fermata/fermata'
  shim:
    bootstrap:
      deps: [ 'jquery' ]
    humanize:
      deps: [ 'jquery' ]
    ridster:
      deps: [ 'jquery' ]
    ko_mapping:
      deps: [ 'knockout' ]
    fermata:
      exports: 'fermata'


@requireVM = (module) ->
  (callback) ->
    require ["/pages/#{module}.js"], (vm) ->
      callback new vm()


@requireHTML = (module) ->
  (page, callback) ->
    require ["text!/pages/#{module}.html"], (html) ->
      $(page.element).html html
      callback()


require ['jquery', 'knockout', 'pager', 'api', 'utils', 'bootstrap'], \
        ($, ko, pager, api, utils) ->
  class Main extends utils.LoadingModel
    constructor: ->
      pager.extendWithPage @
      pager.onBindingError.add (event) ->
        console.error event.error

      @user = ko.observable null

      @ui_displayMainMenu = ko.computed =>
        @configured() == true and @username() != ""


    # check whether the current user is logged in or not
    # redirect to login page, if not logged in
#    isLoggedIn: (page, route, callback) =>
#      $.ajax
#        url: '/_auth/getlogin'
#        dataType: 'json'
#        success: (result) =>
#          if result.success == true
#            @username result.username
#            callback()
#          else
#            window.location.href = "/#system/login";
#        error: (jqXHR, status, error) =>
#          @error error
#          window.location.href = "/#system/login";


    authenticated: () ->
      return @user() == null


    login: (username, password) ->
      api.token.post
        username: username
        password: password,
        (err, res) ->
          if err?
            console.error 'Login failed', err

          else
            console.trace 'User logged in', res

            # Update the user model
            ko.mapping.fromJS res, @user


    logout: () ->
      api.token.delete (err, res) ->
        # Get rid of the user model
        @user null

        # Redirect to the login page
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




  main = new Main

  ko.applyBindings main
  
  main.checkInitialConf()

  
  pager.start()
