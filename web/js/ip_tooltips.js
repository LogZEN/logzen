/*
 * Copyright 2012 Sven Reissmann <sven@0x80.io>
 *
 * This file is part of pyLogView. It is licensed under the terms of the
 * GNU General Public License version 3. See <http://www.gnu.org/licenses/>.
 */

function addIpTooltipTags(string) {
	var ipv4_regex = /(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)\.(([1-9][0-9]{0,2})|0)/;
	var ipv4_revex = /(([1-9][0-9]{0,2})|0)\,(([1-9][0-9]{0,2})|0)\,(([1-9][0-9]{0,2})|0)\,(([1-9][0-9]{0,2})|0)/;
	
	while (ipv4_regex.test(string)) {
		string = string.replace(ipv4_regex, '<span class="tooltip_ip" id="$1,$3,$5,$7">$1,$3,$5,$7</span>');
	}
	while (ipv4_revex.test(string)) {
		string = string.replace(ipv4_revex, '$1.$3.$5.$7');
	}
	return string
}

function loadIpTooltips() {
 	$(".tooltip_ip").each(function() {
 		$(this).qtip({
 			content: {
 				text: 'Loading...',
 				ajax: {
 					url: '/tooltips/ip',
 					type: 'GET',
 					data: { ip: this.id },
 					success: function(data, status) {
 						this.set('content.text', data);
 					}
 				}
 			},
 			position: {
 				my: 'top left',
 				at: 'bottom center'
 			},
 			hide: {
 		        fixed: true,
 				delay: 200
 			},
 			style: {
 				classes: 'ui-tooltip-dark ui-tooltip-shadow ui-tooltip-rounded'
 			}
 		});
 	});
}
