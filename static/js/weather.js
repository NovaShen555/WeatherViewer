var Weather = {
		map: null, // 地图对象
		cityCode: '', // 城市编号
		mapWeatherData: null, // 城市站点数据
		initChart:function(cityName, dateb, datee, maxTempData, minTempData, rainfallData, xAxisData){
			var myChart = echarts.init(document.getElementById('myChart'));
			var option = {
				color: ['#eb6877','#0f91c4','#46cbd4'],
	            title: {
	                subtext: ((dateb == '' || datee == '') ? '' : (dateb + '年-' + datee + '年')) + '月平均气温和降水',
	                left: 20
	            },
	            tooltip: {
			        trigger: 'axis',
			        axisPointer: {
			            type: 'cross'
			        }
			    },
			    grid:{
			    	show: true,
			    	borderColor: '#666',
			    	top:100
			    },
	            legend: {
	                data:['最高气温','最低气温','降水'],
	                right:20
	            },
	            xAxis: {
	                data: xAxisData,
	                axisLine:{
	                	onZero:false
	                }
	            },
	            yAxis: [
	            	{
			            type: 'value',
			            name: '温度',
			            position: 'left',
			            axisLine: {
			                lineStyle: {
			                    color: '#666'
			                }
			            },
			            axisLabel: {
			                formatter: '{value} ℃'
			            }
			        },
			        {
			            type: 'value',
			            name: '降水量',
			            min: 0,
			            position: 'right',
			            axisLine: {
			                lineStyle: {
			                    color: '#666'
			                }
			            },
			            axisLabel: {
			                formatter: '{value} mm'
			            }
			        }
	            ],
	            series: [{
	                name: '最高气温',
	                type: 'line',
	                data: maxTempData,
	                yAxisIndex: 0,
	                itemStyle:{
	                	color:'#eae213'
	                }
	            },{
	                name: '最低气温',
	                type: 'line',
	                smooth: true,
	                data: minTempData,
	                yAxisIndex: 0,
	                itemStyle:{
	                	color:'#4bb2fa'
	                }
	            },{
	                name: '降水',
	                type: 'bar',
	                smooth: true,
	                data: rainfallData,
	                yAxisIndex: 1,
	                barWidth:'auto',
	                itemStyle:{
	                	color:'#31e84f',
	                }
	            }]
	        };
	
	        myChart.setOption(option);
		},
		/**
		 * 获取地图天气数据
		 * <pre>
		 * 如果数据已经加载过，则不再重复加载
		 * </pre>
		 */
		getMapWeatherData: function(callback){
			var self = this;
			if(self.mapWeatherData == null) {
				$.getJSON('/api/map/worldmap?t=' + new Date().getTime(), function(ret){
					self.mapWeatherData = ret.data;
					callback();
				});
			} else {
				callback();
			}
		},
		initMap:function(cityCode, latlng) {
			this.cityCode = cityCode;
			this.map = L.map('map', {
				center: latlng,
		        zoomControl:true,
		        zoom: 4,
		        minZoom:3,
				attributionControl: false
		    });
			
			// 图幅号
			var sheetNumber = 'GS(2018)1432号 - 甲测资字1100471';
			
			// 图幅号控件类
			L.Control.SheetControl = L.Control.extend({
				initialize: function (options) {
			        this._options = options;
			        L.Util.setOptions(this, options);
			    },
			    onAdd: function (map) {
			        var container = L.DomUtil.create('div', 'sheet-control', $('#mapWrap').get(0));
			        container.innerHTML = '<img src="https://api.tianditu.gov.cn/v4.0/image/logo.png" width="53px" height="22px" opacity="0"><div class="sheetNumber" style="position:absolute;bottom:0px;left:58px;white-space:nowrap;">'+sheetNumber+'</div>';
			        return container;
			    }
			});
			var sheetControl = new L.Control.SheetControl({position: 'bottomleft',maptype:this.mapType});
			this.map.addControl(sheetControl);
			
			// 地图
			this.tileLayerGroup = L.layerGroup([
				L.tileLayer("https://t{s}.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=e57d350959299373a6a2eb6cb7942aa5", {
			        subdomains: ["0", "1", "2", "3", "4", "5", "6", "7"]
			    }),
			    L.tileLayer("https://t{s}.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILECOL={x}&TILEROW={y}&TILEMATRIX={z}&tk=e57d350959299373a6a2eb6cb7942aa5", {
				        subdomains: ["0", "1", "2", "3", "4", "5", "6", "7"]
				})
			]);
		    this.tileLayerGroup.addTo(this.map);
		    this.drawMarker();
		},
		gotoWeatherPage:function(e){
			window.location.href = ctx + '/weather/' + e.target.options.cityCode + '.html';
		},
		drawMarker:function() {
			var self = this;
			this.getMapWeatherData(function() {
				var stations = self.mapWeatherData;
				self.weatherLayerGroup = L.layerGroup();
				var latlng = null;
				for(var i in stations) {
					var point = stations[i];
					if(point.location.id == self.cityCode){
						var myIcon = L.icon({
						    iconUrl: '/assets/ydyl/img/location2.png',
						    iconSize: [31, 31]
						});
						latlng = [point.location.latitude, point.location.longitude];
						L.circleMarker(latlng,{cityCode:point.location.id, radius:5, stroke:false, fillOpacity:1, fillColor: '#ff4a53'}).bindTooltip(point.location.name).on('click',function(e){self.gotoWeatherPage(e);}).addTo(self.weatherLayerGroup);
						L.marker([point.location.latitude, point.location.longitude], {cityCode:point.location.id, icon: myIcon}).bindTooltip(point.location.name).on('click',function(e){self.gotoWeatherPage(e);}).addTo(self.weatherLayerGroup);
					} else {
						L.circleMarker([point.location.latitude, point.location.longitude],{cityCode:point.location.id, radius:5, stroke:false, fillOpacity:1}).bindTooltip(point.location.name).on('click',function(e){self.gotoWeatherPage(e);}).addTo(self.weatherLayerGroup);
					}
					
				}
				self.weatherLayerGroup.addTo(self.map);
			});
		}
};