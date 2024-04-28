var CMA = {
		init : function() {
			var self = this;
			
			// 站点类型选择：国内｜国外
			$('.type-select > li').click(function(){
				var $this = $(this);
				var type = $this.data('value');
				var text = $this.text();
				console.log("click")
				$this.parent().parent().find(' > button > span:eq(0)').text(text);
				self.updateCountrySelect(type);
			});
			
			// 国家或省份选择
			$(document).on("click",".province-select > li",function(){
				var $this = $(this);
				var code = $this.data('value');
				var type = $this.data('type');
				var name = $this.text();
				$this.parent().parent().find(' > button > span:eq(0)').text(name);
				self.updateCitySelect(type, code);
			}); 
		},
		updateCountrySelect : function(type) {
			var url = 'https://weather.cma.cn/api/dict/province';
			if(type == '1') {
				url = 'https://weather.cma.cn/api/dict/country';
			}
			$.getJSON(url, function(ret){
				if(ret.code == 0){
					var arr = ret.data.split('|');
					console.log(arr);
					var html = [];
					for(var i = 0; i < arr.length; i++) {
						var s = arr[i].split(',')
						html.push('<li data-type="' + type + '" data-value="' + s[0] + '">' + s[1] + '</li>');
					}
					$('.province-select').html(html.join('')).parent().find(' > button').trigger('click');
				}
			});
		},
		updateCitySelect : function(type, code) {
			var url = 'https://weather.cma.cn/api/dict/province/' + code;
			if(type == '1') {
				url = 'https://weather.cma.cn/api/dict/country/' + code;
			}
			$.getJSON(url, function(ret){
				if(ret.code == 0){
					var arr = ret.data.indexOf('|') > -1 ? ret.data.split('|') : [ret.data];
					
					var html = [];
					for(var i = 0; i < arr.length; i++) {
						var s = arr[i].split(',')
						html.push('<li><a href="/weather/' + s[0] + '.html">' + s[1] + '</a></li>');
					}
					console.log(html)
					$('.station-select').html(html.join('')).parent().find(' > button').trigger('click');
				}
			});
		},
		/**
		 * 获取指定站点ID的天气实况
		 */
		getNow : function(stationid){
			$.getJSON('https://weather.cma.cn/api/now/' + stationid, function(ret){
				if(ret.code == 0 && ret.data) {
						$('#pubtime').text(ret.data.lastUpdate + '更新');
						$('#temperature').html((ret.data.now.temperature >= 9999 ? '-' : ret.data.now.temperature) + '<sup>℃</sup>');
						$('#pressure').text((ret.data.now.pressure >= 9999 ? '-' : ret.data.now.pressure) +'hPa');
						$('#humidity').text((ret.data.now.humidity >= 9999 ? '-' : ret.data.now.humidity) +'%');
						$('#precipitation').text((ret.data.now.precipitation >= 9999) ? '-' :  (ret.data.now.precipitation + 'mm'));
						$('#wind').text( (ret.data.now.windDirection >= 9999 ? '-' : ret.data.now.windDirection) +' ' + (ret.data.now.windScale >= 9999 ? '-' : ret.data.now.windScale));
						
						if(ret.data.alarm.length > 0) {
							var alarmHtml = [];
							for(var i = 0; i < ret.data.alarm.length; i++){
								var alarm = ret.data.alarm[i];
								alarmHtml.push('<a href="/alarm/' + alarm.id + '.html" title="' + alarm.title + '"><img style="height:32px;" src="http://data.cma.cn/dataGis/static/ultra/img/gis/disasterWarning/' + alarm.eventType + '_' + alarm.severity + '.png" onerror="this.src=\'http://data.cma.cn/dataGis/static/ultra/img/gis/disasterWarning/11B99_' + alarm.severity + '.png\'"/></a>');
								break;
							}
							$('#temperature').append('<div class="alarm">' + alarmHtml.join('') + '</div>');
						}
				} else {
					$('#pubtime').text('更新');
					$('#temperature').html(' - <sup>℃</sup>');
					$('#pressure').text(' - ');
					$('#humidity').text(' - ');
					$('#precipitation').text(' - ');
					$('#wind').text(' - ');
					console.log('天气实况获取失败,' + stationid);
				}
			});
		}
};