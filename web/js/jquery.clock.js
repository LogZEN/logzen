/*
Copyright 2012 Sven Reissmann <sven@0x80.io>

This file is part of pyLogView. It is licensed under the terms of the 
GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
*/

(function(jQuery) {
	jQuery.fn.clock = function(options) {
		var defaults = {
			offset: '+0'
		};
		var _this = this;
		var opts = jQuery.extend(defaults, options);
		
		function refreshClock() {
			var hours = jQuery.calcTime(opts.offset).getHours();
			var minutes = jQuery.calcTime(opts.offset).getMinutes();
			var seconds = jQuery.calcTime(opts.offset).getSeconds();
			
			if (hours < 10) hours = '0' + hours;
			if (minutes < 10) minutes = '0' + minutes;
			if (seconds < 10) seconds = '0' + seconds;
			
			jQuery(_this).find(".hour").html(hours + ':');
			jQuery(_this).find(".min").html(minutes + ':');
			jQuery(_this).find(".sec").html(seconds);
		}
		refreshClock()
		setInterval(refreshClock, 1000);
	}
})(jQuery);

jQuery.calcTime = function(offset) {
	d = new Date();
	utc = d.getTime() + (d.getTimezoneOffset() * 60000);
	nd = new Date(utc + (3600000 * offset));
	return nd;
};
