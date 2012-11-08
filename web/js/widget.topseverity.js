// Generated by CoffeeScript 1.3.3

/*
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
*/


(function() {
  var TopSeverity, TopSeverityView;

  TopSeverity = (function() {

    function TopSeverity() {
      var _this = this;
      this.hostSelected = ko.observable(null);
      this.hosts = ko.observableArray([]);
      this.severities = {
        '0': ko.observable(0),
        '1': ko.observable(0),
        '2': ko.observable(0),
        '3': ko.observable(0),
        '4': ko.observable(0),
        '5': ko.observable(0),
        '6': ko.observable(0),
        '7': ko.observable(0)
      };
      this.severitySum = ko.computed(function() {
        var severity, sum, value, _ref;
        sum = 0;
        _ref = _this.severities;
        for (severity in _ref) {
          value = _ref[severity];
          sum += value();
        }
        return sum;
      });
      this.query = ko.computed(function() {
        return cs({
          'query': {
            'match_all': {}
          },
          'from': 0,
          'size': 0,
          'facets': {
            'hosts': {
              'terms': {
                'field': 'host'
              }
            },
            'severities': {
              'terms': {
                'field': 'severity'
              },
              'facet_filter': cs["if"](_this.hostSelected, {
                'term': {
                  'host': _this.hostSelected()
                }
              }, {})
            }
          }
        });
      });
      ko.computed(function() {
        return $.ajax({
          url: "/_api/query",
          type: 'POST',
          contentType: "application/json",
          data: JSON.stringify(_this.query()()),
          dataType: 'json',
          success: function(result) {
            var chart1, chart_data, data, host, severities, severity, value, _i, _len, _ref, _ref1;
            _this.hosts((function() {
              var _i, _len, _ref, _results;
              _ref = result.facets.hosts.terms;
              _results = [];
              for (_i = 0, _len = _ref.length; _i < _len; _i++) {
                host = _ref[_i];
                _results.push(host.term);
              }
              return _results;
            })());
            severities = {};
            _ref = result.facets.severities.terms;
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              severity = _ref[_i];
              severities[severity.term] = severity.count;
            }
            _ref1 = _this.severities;
            for (severity in _ref1) {
              value = _ref1[severity];
              value(severities[severity] || 0);
            }
            data = (function() {
              var _j, _len1, _ref2, _results;
              _ref2 = result.facets.severities.terms;
              _results = [];
              for (_j = 0, _len1 = _ref2.length; _j < _len1; _j++) {
                severity = _ref2[_j];
                _results.push({
                  'label': Defaults.severity[severity.term],
                  'value': severity.count
                });
              }
              return _results;
            })();
            chart_data = [
              {
                key: "severity",
                values: data
              }
            ];
            chart1 = nv.models.pieChart().x(function(d) {
              return d.label;
            }).y(function(d) {
              return d.value;
            }).showLabels(true);
            d3.select("#topseverity svg").datum(chart_data).transition().duration(200).call(chart1);
            return nv.utils.windowResize(chart1.update);
          }
        });
      });
    }

    return TopSeverity;

  })();

  TopSeverityView = new TopSeverity;

  ko.applyBindings(TopSeverityView, $('#widget_topseverity').get(0));

}).call(this);
