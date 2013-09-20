// Generated by CoffeeScript 1.6.3
/*
Copyright 2013 Sven Reissmann <sven@0x80.io>

This file is part of LogZen. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
*/


(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };

  define(['jquery', 'knockout', 'pager', 'vars', 'bootstrap', 'prettyjson'], function($, ko, pager, vars) {
    var EventListModel, EventModel, pivot;
    pivot = function(key, value, data) {
      var result;
      result = {};
      result[data[key]] = data[value];
      return result;
    };
    EventModel = (function() {
      function EventModel(data) {
        this.id = data._id;
        this.time = data._source.time;
        this.facility = data._source.facility;
        this.facility_text = ko.computed(function() {
          return vars.facility[data._source.facility];
        });
        this.severity = data._source.severity;
        this.severity_text = ko.computed(function() {
          return vars.severity[data._source.severity];
        });
        this.detail_url = "/event/" + data._id;
        this.host = data._source.host;
        this.program = data._source.program;
        this.message = data._source.message;
        this.message_hl = this.markIP(data._source.message);
      }

      EventModel.prototype.markIP = function(msg) {
        var ipv4_regex;
        ipv4_regex = /((([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0))/g;
        return msg.replace(ipv4_regex, '<span class="tooltip_ip">$1</span>');
      };

      return EventModel;

    })();
    EventListModel = (function() {
      function EventListModel() {
        this.refreshPage = __bind(this.refreshPage, this);
        this.nextPage = __bind(this.nextPage, this);
        this.prevPage = __bind(this.prevPage, this);
        this.clearFilter = __bind(this.clearFilter, this);
        this.setFilter = __bind(this.setFilter, this);
        this.loadEvents = __bind(this.loadEvents, this);
        var _this = this;
        this.events = ko.observableArray([]);
        this.hits = 0;
        this.loading = ko.observable(false);
        this.page = ko.observable(0);
        this.error = ko.observable(null);
        this.refreshId = ko.observable(setInterval(this.loadEvents, 5000));
        this.filterMode = ko.observable("fields");
        this.freetextValue = ko.observable("");
        this.freetextValueFormatted = ko.observable("");
        this.filters = {
          'severity': ko.observable(""),
          'facility': ko.observable(""),
          'host': ko.observable(""),
          'program': ko.observable(""),
          'message': ko.observable("")
        };
        this.filledFilters = ko.computed(function() {
          var filter, name, _ref, _results;
          _ref = _this.filters;
          _results = [];
          for (name in _ref) {
            filter = _ref[name];
            if (filter() !== '') {
              _results.push({
                'name': name,
                'value': filter()
              });
            }
          }
          return _results;
        });
        this.freetext = ko.computed({
          read: function() {
            var f, filter, first, _i, _len, _ref;
            if (_this.filterMode() === 'fields') {
              f = '';
              if (_this.filledFilters().length > 0) {
                first = 1;
                _ref = _this.filledFilters();
                for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                  filter = _ref[_i];
                  if (first !== 1) {
                    f = f + ',';
                  }
                  first = 0;
                  f = f + '{ "prefix": { "' + filter['name'] + '": "' + filter['value'] + '" } }';
                }
                console.log(f);
                f = ',\
                "filter": {\
                  "and": [ ' + f + '\
                  ]\
                }';
              }
              f = '\
            {\
              "query": { \
                "filtered": {\
                  "query": {\
                    "match_all" : {}\
                  }' + f + '\
                }\
              },\
              "from": ' + _this.page() * 50 + ',\
              "size":  50 ,\
              "sort": [{\
                "time": {\
                  "order": "desc"\
                }\
              }]\
            }';
              _this.freetextValue(f);
              console.log(_this.freetextValue());
              _this.freetextValueFormatted(pj(f));
              return _this.loadEvents();
            }
          },
          write: function(value) {
            console.log(_this.freetextValue());
            return _this.freetextValue(value.replace(/<\*>/g, ""));
          }
        });
      }

      EventListModel.prototype.loadEvents = function() {
        var _this = this;
        if (this.filterMode() === 'fields') {
          return $.ajax({
            url: $('#filterform').attr('action'),
            type: 'POST',
            contentType: "application/json",
            data: this.freetextValue(),
            dataType: 'json',
            beforeSend: function() {
              return _this.loading(true);
            },
            success: function(result) {
              var event;
              _this.loading(false);
              _this.error(null);
              _this.hits = result.hits.total;
              _this.events((function() {
                var _i, _len, _ref, _results;
                _ref = result.hits.hits;
                _results = [];
                for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                  event = _ref[_i];
                  _results.push(new EventModel(event));
                }
                return _results;
              })());
              return _this.addTooltips();
            },
            error: function(jqXHR, status, error) {
              _this.loading(false);
              _this.error(error);
              _this.hits = 0;
              return _this.events([]);
            }
          });
        }
      };

      EventListModel.prototype.setFilter = function(name) {
        var _this = this;
        return function(el) {
          return _this.filters[name](el[name]);
        };
      };

      EventListModel.prototype.clearFilter = function(name) {
        var _this = this;
        return function() {
          return _this.filters[name]("");
        };
      };

      EventListModel.prototype.prevPage = function() {
        if (this.page() > 0) {
          return this.page(this.page() - 1);
        }
      };

      EventListModel.prototype.nextPage = function() {
        if (this.page() * 50 + 50 < this.hits) {
          return this.page(this.page() + 1);
        }
      };

      EventListModel.prototype.refreshPage = function() {
        if (this.refreshId() === -1) {
          return this.refreshId(setInterval(this.loadEvents, 5000));
        } else {
          clearInterval(this.refreshId());
          return this.refreshId(-1);
        }
      };

      EventListModel.prototype.timeSeries = function(data) {
        var chart;
        chart = nv.models.multiBarTimeSeriesChart().x(function(d) {
          return d.time;
        }).y(function(d) {
          return d.count;
        });
        chart.xAxis.tickFormat(function(d) {
          return d3.time.format('%x')(new Date(d));
        }).rotateLabels(-45);
        chart.yAxis.tickFormat(d3.format(',.0f'));
        chart.tooltip = function(key, x, y, e, graph) {
          return '<h3>#{key}</h3><p>#{y} during #{x}</p>';
        };
        d3.select('#timeSeries svg').datum([
          {
            "key": "events",
            "values": data
          }
        ]).transition().duration(100).call(chart);
        return nv.utils.windowResize(chart.update);
      };

      EventListModel.prototype.addTooltips = function() {
        var _this = this;
        return $('.tooltip_ip').each(function(index, element) {
          var el;
          el = $(element);
          return el.bind('mouseenter', function() {
            return $.ajax({
              url: '/_tooltip/ip',
              type: 'POST',
              data: 'ip=' + el.text(),
              dataType: 'json',
              success: function(result) {
                var html;
                html = '\
                <table>\
                  <tr><td>IP Address</td><td>' + result.ip + '</td></tr>\
                  <tr><td>DNS Name</td><td> ' + result.dns + '</td></tr>\
              ';
                if (result.aliaslist !== "") {
                  html += '<tr><td>Aliases</td><td> ' + result.aliaslist + '</td></tr>';
                }
                if (result.addresslist !== "") {
                  html += '<tr><td>Addresses</td><td> ' + result.addresslist + '</td></tr>';
                }
                html += '\
                  <tr><td>Country</td><td>' + result.country + ' <img src="/img/flags/' + result.flagimg + '.gif" title="' + result.country + '" alt="' + result.country + '"/></td></tr>\
                </table>\
              ';
                el.attr('data-toggle', 'tooltip');
                el.attr('data-original-title', html);
                el.tooltip({
                  content: "dynamic text",
                  html: true,
                  trigger: 'hover',
                  container: 'body'
                });
                return el.tooltip('show');
              }
            });
          });
        });
      };

      return EventListModel;

    })();
    return EventListModel;
  });

}).call(this);
