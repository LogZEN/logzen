###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout'], \
       ($, ko) ->
  class LoginModel
    constructor: ->
      @username = ko.observable ""
      @password = ko.observable ""
      
      @submitOK = ko.computed () =>
        if @username() != "" and @password() != ""
          true
        else
          false


    login: ->
      $.ajax
        url: '/_auth/login'
        type: 'POST'
        data: 'username=' + @username() + '&password=' + @password()
        dataType: 'json'
        success: (result) =>
          if result.success == 'true'
            @username result.username
            window.location.href = "/";


  LoginModel
