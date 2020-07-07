function accept_request(id){
	xhr= new XMLHttpRequest();
	console.log("new State: ", xhr.readyState);

	url= `/accept_request/id=${id}`;
	xhr.open('GET', url, true);
	console.log("open State: ", xhr.readyState);

	xhr.onreadystatechange= function(){
		console.log("in onready State: ", xhr.readyState);
		if(this.readyState == this.DONE && this.status == 200){
			response= JSON.parse(this.responseText);
			if(response.success === true){ 
				button_id= `accept_${id}`;
				console.log('button_id: ', button_id);

				let button= document.getElementById(button_id);
				button.remove();
				delete_button= document.getElementById(`delete_${id}`);
				if( delete_button != null){
					delete_button.remove();
				}

				//
				document.getElementById('about_me').innerHTML = 'successfull accept';
			}
			else{
				alert(response.success);
			}
		}
		else if(this.status == 404){
			document.getElementById('about_me').innerHTML = 'Not Found';
		}
	};

	xhr.send();
	console.log("State: ", xhr.readyState);	
}		

// -------------------------------------------------------------------


function delete_request(id){
	xhr= new XMLHttpRequest();
	console.log("new State: ", xhr.readyState);

	url= `/delete_request/id=${id}`;
	xhr.open('GET', url, true);
	console.log("open State: ", xhr.readyState);

	xhr.onreadystatechange= function(){
		console.log("in onready State: ", xhr.readyState);
		if(this.readyState == this.DONE && this.status == 200){
			response= JSON.parse(this.responseText);
			if(response.success === true){ 
				button_id= `delete_${id}`;
				console.log('button_id: ', button_id);

				button= document.getElementById(button_id);

				button.setAttribute('onclick', `send_request(${id})`);

				button.classList.remove('delete_button');
				button.classList.add('send_button');
				
				button.id= `send_${id}`;
				button.innerHTML= 'Send Request';

				accept_button= document.getElementById(`accept_${id}`);
				if( accept_button != null){
					accept_button.remove();
				}
				// 
				document.getElementById('about_me').innerHTML = 'success delete';
			}
			else{
				alert(response.success);
			}
		}
		else if(this.status == 404){
			document.getElementById('about_me').innerHTML = 'Not Found';
		}
	};

	xhr.send();
	console.log("State: ", xhr.readyState);	
}

// -------------------------------------------------------

function send_request(id){
	xhr= new XMLHttpRequest();
	console.log("new State: ", xhr.readyState);

	url= `/send_request/id=${id}`;
	xhr.open('GET', url, true);
	console.log("open State: ", xhr.readyState);

	xhr.onreadystatechange= function(){
		console.log("in onready State: ", xhr.readyState);
		if(this.readyState == this.DONE && this.status == 200){
			response= JSON.parse(this.responseText);
			if(response.success === true){ 
				button_id= `send_${id}`;
				console.log('button_id: ', button_id);

				let button= document.getElementById(button_id);
				button.classList.remove('send_button')
				button.classList.add('delete_button');

				button.setAttribute('onclick', `delete_request(${id})`);

				button.id= `delete_${id}`;
				button.innerHTML= 'Delete Request';
				// 
				document.getElementById('about_me').innerHTML = 'success send';
			}
			else{
				alert(response.success);
			}
		}
		else if(this.status == 404){
			document.getElementById('about_me').innerHTML = 'Not Found';
		}
	};

	xhr.send();
	console.log("State: ", xhr.readyState);	
}		
