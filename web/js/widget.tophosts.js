// Generated by CoffeeScript 1.3.3

/*
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
*/


(function() {
  var TopHosts, view;

  TopHosts = (function() {

    function TopHosts() {
      this.qry = {
        "query": {
          "match_all": {}
        },
        "from": 0,
        "size": 0,
        "sort": [],
        "facets": {
          "byhost": {
            "terms": {
              "field": "hostname"
            }
          }
        }
      };
    }

    TopHosts.prototype.load = function() {
      var _this = this;
      return $.ajax({
        url: "/_api/query",
        dataType: 'json',
        type: 'POST',
        contentType: "application/json",
        data: JSON.stringify(this.qry),
        success: function(result) {
          var chart1, chart2, chart_data, data, next;
          data = (function() {
            var _i, _len, _ref, _results;
            _ref = result.facets.byhost.terms;
            _results = [];
            for (_i = 0, _len = _ref.length; _i < _len; _i++) {
              next = _ref[_i];
              _results.push({
                label: next['term'],
                value: next['count']
              });
            }
            return _results;
          })();
          chart_data = [
            {
              key: "events",
              values: data
            }
          ];
          chart1 = nv.models.pieChart().x(function(d) {
            return d.label;
          }).y(function(d) {
            return d.value;
          }).showLabels(true);
          d3.select("#events_by_host svg").datum(chart_data).transition().duration(200).call(chart1);
          chart2 = nv.models.discreteBarChart().x(function(d) {
            return d.label;
          }).y(function(d) {
            return d.value;
          }).staggerLabels(true);
          d3.select('#top_hosts svg').datum(chart_data).transition().duration(200).call(chart2);
          nv.utils.windowResize(chart1.update);
          return nv.utils.windowResize(chart2.update);
        }
      });
    };

    return TopHosts;

  })();

  view = new TopHosts;

  view.load();

  ko.applyBindings(view);

}).call(this);
