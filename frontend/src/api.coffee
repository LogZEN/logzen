###
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
###

define ['jquery', 'knockout'], \
       ($, ko) ->
  class Resource
    constructor: (path) ->
      @path = "/api/v1/#{path}"

    get: () ->
      $.ajax @path,
        type: 'GET'
        accepts: 'json'

    post: (data) ->
      $.ajax @path,
        type: 'POST'
        contentType: 'application/json'
        accepts: 'application/json'
        data: ko.toJSON data

    delete: () ->
      $.ajax @path,
        type: 'DELETE'
        accepts: 'application/json'


  return (path) ->
    return new Resource path




