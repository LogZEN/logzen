###
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout', 'index'], \
       ($, ko, index) ->
  class LoginModel
    constructor: () ->
      @username = ko.observable ''
      @password = ko.observable ''
      
      @submitable = ko.computed () =>
        @username() != '' and @password() != ''


    login: () ->
      index.login @username(), @password()


  return LoginModel
