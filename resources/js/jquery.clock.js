/* Copyright (c) 2009 José Joaquín Núñez (josejnv@gmail.com) http://joaquinnunez.cl/blog/
 * Licensed under GPL (http://www.opensource.org/licenses/gpl-2.0.php)
 * Use only for non-commercial usage.
 *
 * Version : 0.1
 *
 * Requires: jQuery 1.2+
 */

(function(jQuery) {
	jQuery.fn.clock = function(options) {
		var defaults = {
			offset: '+0'
		};
		var _this = this;
		var opts = jQuery.extend(defaults, options);
		
		setInterval( function() {
			var seconds = jQuery.calcTime(opts.offset).getSeconds();
			var minutes = jQuery.calcTime(opts.offset).getMinutes();
			var hours = jQuery.calcTime(opts.offset).getHours();
			
			if (seconds < 10) seconds = '0' + seconds;
			if (minutes < 10) minutes = '0' + minutes;
			if (hours < 10) hours = '0' + hours;
			
			jQuery(_this).find(".sec").html(seconds);
			jQuery(_this).find(".hour").html(hours + ':');
			jQuery(_this).find(".min").html(minutes + ':');
		}, 1000 );
	}
})(jQuery);


jQuery.calcTime = function(offset) {
	d = new Date();
	utc = d.getTime() + (d.getTimezoneOffset() * 60000);
	nd = new Date(utc + (3600000*offset));
	return nd;
};
