/**
 * Created by Developer on 7/3/2016.
 */
(function (window, $, undefined) {

	window.APPLICATION = {
		JSON_msg: new Object(),
		// websocket object
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
				var received_message =  JSON.parse(event.data);
				var html =
					"<div  class=\"row message\">"
					+"<div class=\"col-xs-2 \">" + received_message.name  + "</div>"
					+"<div  class=\"col-xs-10 \">"+ received_message.data + "</div>"
					+"</div>"
			


				$("#receive").append(html)
			};

		},

		onSend: function () {
		var nickname = 	$("#client_nick_name").val();
		var message = 	$("#message").val();



			this.JSON_msg.name = nickname
			this.JSON_msg.data = message


		this.GLOBAL_ws.send(JSON.stringify(this.JSON_msg));

		}

	}


})(window, jQuery)