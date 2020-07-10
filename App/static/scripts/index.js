function get_chat(id){
	xhr= new XMLHttpRequest();
	// console.log("new State: ", xhr.readyState);

	url= `/get_chat/id=${id}`;
	xhr.open('GET', url, true);
	// console.log("open State: ", xhr.readyState);
	xhr.onreadystatechange= function(){
		// console.log("in onready State: ", xhr.readyState);
		if(this.readyState == this.DONE && this.status == 200){
			response= JSON.parse(this.responseText);
			if(response.success === true){ 
				// document.getElementById('default_chat').remove()

				chat=  response.chat;
				div= document.getElementById('chat');
				div.innerHTML="";
				div.innerHTML= chat;
			}
			else{
				alert(response.success);
			}
		}
		else if(this.status == 404){
			document.getElementById('about_me').innerHTML = 'Not Found';
		}
	}
	xhr.send();
}

function send_message(id){
		xhr= new XMLHttpRequest();
	// console.log("new State: ", xhr.readyState);

	url= "/send_message";
	id= parseInt(document.getElementById("send").value);
	message= document.getElementById("message_area").value;
	// console.log(message);
	var params = `message=${message}&id=${id}`;

	xhr.open('POST', url, true);

	//Send the proper header information along with the request
	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

	// console.log("open State: ", xhr.readyState);
	xhr.onreadystatechange= function(){
		// console.log("in onready State: ", xhr.readyState);
		if(this.readyState == this.DONE && this.status == 200){
			success= JSON.parse(this.responseText);
			if(success === true){ 
				// document.getElementById('default_chat').remove()
				get_chat(id);
				document.getElementById(`last_message_${id}`).innerHTML= `you: ${message}`	
			}
			else{
				alert(response.success);
			}
		}
		else if(this.status == 404){
			document.getElementById('about_me').innerHTML = 'Not Found';
		}
	}
	xhr.send(params);
}