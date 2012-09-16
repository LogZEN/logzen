/*
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
 */
(function(jQuery) {
	jQuery.fn.clock = function() {
		var _this = this
		
		function refreshClock() {
			d = new Date();
			var hours = d.getHours();
			var minutes = d.getMinutes();
			var seconds = d.getSeconds();
			var offset = -(d.getTimezoneOffset() / 60)

			if (hours < 10) hours = '0' + hours;
			if (minutes < 10) minutes = '0' + minutes;
			if (seconds < 10) seconds = '0' + seconds;
			if (offset > 0) offset = '+' + offset
			
			$(_this).html(hours + ':' + minutes + ':' + seconds + ' GMT' + offset);
		}
		refreshClock()
		setInterval(refreshClock, 1000);
	}
})(jQuery);