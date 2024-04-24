var ImagePlayer = {
		index: 0, // 当前显示索引号
		imgTotalNum: 2, // 图片总数
		timer: null, // 定时器
		init: function(totalNum) {
			this.imgTotalNum = totalNum;
			this.bindEvent();
			this.show(this.index);
		},
		bindEvent: function(){
			var self = this;
			$('#prev').click(function(){
				self.stop();
				self.prev();
			});
			$('#next').click(function(){
				self.stop();
				self.next();
			});
			$('#player').click(function(){
				if(self.timer == null) {
					self.player();
				} else {
					self.stop();
				}
			});
			$('#timeList').change(function(){
				self.stop();
				var idx = $(this).get(0).selectedIndex;
				self.show(idx);
			});
		},
		show: function(idx) {
			var sel = $('#timeList >option:eq(' + idx + ')');
			$('#imgPath').attr('src', sel.val());
			$('#zoom').attr('href', sel.val());
			sel.attr('selected', true);
			$('#progressBar').css('width', (((this.imgTotalNum - idx) / this.imgTotalNum) * 100 + '%'));
			this.index = idx;
		},
		prev: function(){
			var idx = (this.index + 1) >= this.imgTotalNum ? 0 : (this.index + 1);
			this.show(idx);
		},
		next: function(){
			var idx = (this.index - 1) >= 0 ? (this.index - 1) : (this.imgTotalNum - 1);
			this.show(idx);
		},
		player: function(){
			var self = this;
			$('#player').removeClass('icon-play').addClass('icon-stop');
			this.timer = setInterval(function(){
				self.next();
				if(self.index == 0) {
					self.stop();
				}
			}, 200);
		},
		stop: function(){
			$('#player').removeClass('icon-stop').addClass('icon-play');
			if(this.timer != null) {
				clearInterval(this.timer);
				this.timer = null;
			}
		}
}