###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

require.config
#  urlArgs: 'v=' + new Date()
  baseUrl: '/'
  paths:
    'jquery':'libs/jquery/dist/jquery'
    'knockout':'libs/knockoutjs/dist/knockout.debug'
    'pager':'libs/pagerjs/pager'
    'bootstrap':'libs/bootstrap/dist/js/bootstrap'
    'require.text': 'libs/requirejs-text/text'
    'jquery.gridster': 'libs/gridster/dist/jquery.gridster'
    'jquery.humanize': 'libs/jquery.humanize'
  shim:
    'bootstrap':
      deps: [ 'jquery' ]
    'jquery.humanize':
      deps: [ 'jquery' ]
    'jquery.gridster':
      deps: [ 'jquery' ]


@requireVM = (module, root) ->
  (callback) ->
    require ["/pages/#{module}.js"], (vm) ->
      callback new vm root


@requireHTML = (module) ->
  (page, callback) ->
    require ["require.text!/pages/#{module}.html"], (html) ->
      $(page.element).html html
      callback()


define ['jquery', 'knockout', 'pager', 'api', 'utils', 'bootstrap'], \
        ($, ko, pager, api, utils) ->

  class Main extends utils.LoadingModel
    constructor: ->
      @user = ko.observable null

      @authenticated = ko.computed () =>
        @user() != null


    login: (username, password) ->
      document.cookie = 'logzen.auth=;'

      api('token').post
        username: username
        password: password

      .error (err) =>
        console.error 'Login failed', err

      .done (res) =>
        console.log 'User logged in', res

        # Update the user information
        @user res

        # Redirect to the dashboard
        pager.navigate 'dashboard'


    logout: () ->
      api('token').delete()
      .then () =>
        # Get rid of the user model
        @user null

        # Redirect to the login page
        pager.navigate 'system/login'



  main = new Main

  pager.extendWithPage main
  pager.onBindingError.add console.error
  pager.start()

  ko.applyBindings main

  return main
