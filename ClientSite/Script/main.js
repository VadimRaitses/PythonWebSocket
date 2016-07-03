/**
 * Created by Developer on 7/3/2016.
 */
(function (window, $, undefined) {

	window.APPLICATION = {

	    msg : { event: 'register' },


		GLOBAL_ws: null,


		init: function () {

			//debugger;
			//for(i=0;i<20;i++) {
			//	console.log("i: "+i)
				GLOBAL_ws = new WebSocket("ws://localhost:12345")
			//}
			GLOBAL_ws.onopen = function () {
			//	debugger;
				console.log("Opening a connection...");
				window.identified = false;
				//ws.send("Here's some text that the server is urgently awaiting!");
			};

			GLOBAL_ws.onclose = function (evt) {
			//	debugger;
				console.log("I'm sorry. Bye!");
			};

			GLOBAL_ws.onerror = function (evt) {
				//debugger;
				console.log("ERR: " + evt.data);
			};

			GLOBAL_ws.onmessage = function (event) {
				debugger;
				var html = "<div  class=\"col-xs-12 message\">"
					       +"<div class=\"row\">" + event.data  + "</div></div>"

				$("#receive").append(html)
			};

		},

		onSend: function () {
			//debugger;

		var message = 	$("#message").val();

		GLOBAL_ws.send(JSON.stringify(APPLICATION.msg));

		}

	}


})(window, jQuery)