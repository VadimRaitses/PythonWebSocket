/**
 * Created by Developer on 7/3/2016.
 */
(function (window, $, undefined) {

	window.APPLICATION = {

	    msg : { data: '[]' },


		GLOBAL_ws: null,


		init: function () {


			this.GLOBAL_ws = new WebSocket("ws://localhost:12345")

			this.GLOBAL_ws.onopen = function () {
				console.log("Opening a connection...");
				window.identified = false;
			};

			this.GLOBAL_ws.onclose = function (evt) {
				console.log("Connection Closed");
			};

			this.GLOBAL_ws.onerror = function (evt) {
				console.log("ERR: " + evt.data);
			};

			this.GLOBAL_ws.onmessage = function (event) {
				debugger;
				var html = "<div  class=\"col-xs-12 message\">"
					       +"<div class=\"row\">" + event.data  + "</div></div>"

				$("#receive").append(html)
			};

		},

		onSend: function () {

		var message = 	$("#message").val();

		this.GLOBAL_ws.send(JSON.stringify(APPLICATION.msg).replace('[]',message));

		}

	}


})(window, jQuery)