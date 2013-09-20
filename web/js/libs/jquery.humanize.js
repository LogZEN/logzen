/*
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the 
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
 */
(function($) {
	var methods = {
		datetime: function(timestamp) {
			now = new Date().getTime();
			value = new Date(timestamp).getTime();
			delta = (now - value) / 1000;

	        if (value > now)
	        	ago = 'from now' 
	        else 
	        	ago = 'ago'

    	    seconds = delta
    	    days = delta / (60 * 60 * 24)
    	    years = Math.floor(days / 365)
    	    days = days % 365
    	    months = Math.floor(days / 30.5)
    	    
		    if (years == 0 && days < 1) {
		        if (seconds == 0)
		            delta = "a moment"
		        else if (seconds == 1)
		            delta = "a second"
		        else if (seconds < 60)
		        	delta = Math.floor(seconds) + " seconds"
		        else if (seconds >= 60 && seconds < 120)
		            delta = "a minute"
		        else if (seconds >= 120 && seconds < 3600)
		            delta = Math.floor(seconds / 60) + " minutes"
		        else if (seconds >= 3600 && seconds < 3600 * 2)
		            delta = "an hour"
		        else if (3600 < seconds)
		        	delta = Math.floor(seconds / 3600) + " hours"
		    
		    } else if (years == 0) {
		        if (days == 1)
		        	delta = "a day"
		        else if (months == 0)
		        	delta = Math.floor(days) + " days"
		        else if (months == 1)
		        	delta = "a month"
		        else
		        	delta = Math.floor(months) + " months"
		        	
		    } else if (years == 1) {
		        if (months == 0)
		        	delta = "a year"
		        else
		            if (months == 1)
		            	delta = "1 year, 1 month"
		            else
		            	delta = "1 year, " + Math.floor(months) + " months"
		    
		    } else {
		    	delta = Math.floor(years) + " years"
		    }

		    if (delta == "a moment")
		        return "now"
		    else
		    	return delta + " " + ago
		},
		intcomma: function(value) {
			value += '';
			var rgx = /(\d+)(\d{3})/;
			while (rgx.test(value)) {
				value = value.replace(rgx, '$1' + ',' + '$2');
			}
			return value;
		},
		ordinal: function(value) {
			var n = value % 100;
			var suffix = ['th', 'st', 'nd', 'rd', 'th'];
			var ord = n < 21 ? (n < 4 ? suffix[n] : suffix[0]) : (n % 10 > 4 ? suffix[0] : suffix[n % 10]);
			return value + ord;
		}
	};
	
	$.humanize = function(method) {
		if (methods[method]) {
			return methods[method].apply(this, Array.prototype.slice.call(arguments, 1));
		} else if (typeof method === 'object' || !method) {
			return methods.init.apply(this, arguments);
		} else {
			$.error('Method ' +  method + ' does not exist on jQuery.humanize');
		}
    };
})(jQuery);