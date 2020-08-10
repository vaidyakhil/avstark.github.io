document.addEventListener('DOMContentLoaded', function(){
	// console.log('check')
	socket= io.connect('http://' + document.domain + ':' + location.port);

	username= document.getElementById('username').innerText.trim();

	socket.on('connect', function(){
		socket.send("Am I connected to you server?");
		socket.emit('join', {'name' : username});
	})
	socket.on('acknowledgement', (data) => {
		// console.log("Server: ", data); 
		socket.emit('join', {'name': username});
	})
	socket.on('message', (msg)=> {
		console.log("Received: ", msg);
	})

	document.getElementById('logout').onclick= ()=>{
		socket.emit('leave', {'name' : username});
	}

	socket.on('request received', (data)=>{
		if(data['success']){
			console.log('request received', username, id);	
			id= data['sender']
			button_id= `send_${id}`;

			let button= document.getElementById(button_id);
			button.classList.remove('send_button')
			button.classList.add('delete_button');

			button.onclick= ()=>{
				onclick_delete(socket, username, id);
			};
			button.id= `delete_${id}`;
			button.innerHTML= 'Delete Request';	
			
			accept_button= document.createElement('button')
			accept_button.id= `accept_${id}`
			accept_button.classList.add('user_button')	
			accept_button.classList.add('accept_button')
			accept_button.value=`${id}`
			accept_button.onclick= ()=>{
				onclick_accept(socket, username, id);
			}
			accept_button.innerHTML="Accept Request"
			document.getElementById(`user_upper_detail${id}`).appendChild(accept_button);			
		}	
	})
	
	socket.on('send request response', (data)=>{
		if(data['success']){
			id= data['receiver']
			button_id= `send_${id}`;

			let button= document.getElementById(button_id);
			button.classList.remove('send_button')
			button.classList.add('delete_button');

			button.onclick= ()=>{
				onclick_delete(socket, username, id);
			};

			button.id= `delete_${id}`;
			button.innerHTML= 'Delete Request';	
		}
		else{
			alert("Something unexpected has occured pease refresh the page");
		}
	})

	document.querySelectorAll('.send_button').forEach( (button) =>{
		// console.log(button);
		id= parseInt(button.value);
		button.onclick= ()=>{
			onclick_send(socket, username, id);
		}
	});

	socket.on('request accepted', (data)=>{
		if(data['success']){
			console.log('request accepted ', username, id);
			id= data['sender'];

			delete_button= document.getElementById(`delete_${id}`);
			if( delete_button != null){
				delete_button.remove();
			}
			friend= document.createElement("div");
			friend.innerHTML="Already Friend";
			friend.classList.add("already_friend");
			document.getElementById(`user_upper_detail${id}`).appendChild(friend);
		}
	})
	socket.on('accept request response', (data)=>{
		if(data['success']){
			id= data['receiver']			
			button_id= `accept_${id}`;

			let button= document.getElementById(button_id);
			button.remove();
			delete_button= document.getElementById(`delete_${id}`);
			if( delete_button != null){
				delete_button.remove();
			}

			friend= document.createElement("div");
			friend.innerHTML="Already Friend";
			friend.classList.add("already_friend");
			document.getElementById(`user_upper_detail${id}`).appendChild(friend);
		}
		else{
			alert("Something unexpected has occured pease refresh the page");
		}
	})
	document.querySelectorAll('.accept_button').forEach( (button) =>{
		id= parseInt(button.value);
		button.onclick= ()=>{
			onclick_accept(socket, username, id);
		}
	});

	socket.on('request deleted', (data)=>{
		if(data['success']){
			// console.log('request deleted ', username, id);		
			id= data['sender']
			button_id= `delete_${id}`;

			if(document.getElementById(button_id) != null){
				let button= document.getElementById(button_id);

				button.classList.remove('delete_button')
				button.classList.add('send_button');

				button.onclick= ()=>{
					onclick_send(socket, username, id);
				};
				button.id= `send_${id}`;
				button.innerHTML= 'Send Request';

				accept_button= document.getElementById(`accept_${id}`);
				if( accept_button != null){
					accept_button.remove();
				}	
			}
			else{
				send_button= document.createElement('button')
				send_button.id= `send_${id}`
				send_button.classList.add('user_button')	
				send_button.classList.add('send_button')
				send_button.value=`${id}`
				send_button.onclick= ()=>{
					onclick_send(socket, username, id);
				}
				send_button.innerHTML="Send Request"
				document.getElementById(`user_upper_detail${id}`).appendChild(send_button);
			}	
		}	
	})

	socket.on('delete request response', (data)=>{
		if(data['success']){
			id= data['receiver']
			button_id= `delete_${id}`;

			button= document.getElementById(button_id);
			button.classList.remove('delete_button');
			button.classList.add('send_button');

			button.onclick= ()=>{
				onclick_send(socket, username, id);
			};
			button.id= `send_${id}`;
			button.innerHTML= 'Send Request';

			accept_button= document.getElementById(`accept_${id}`);
			if( accept_button != null){
				accept_button.remove();
			}
		}
		else{
			alert("Something unexpected has occured pease refresh the page");
		}
	})
	document.querySelectorAll('.delete_button').forEach( (button) =>{
		id= parseInt(button.value);
		button.onclick= ()=>{
			onclick_delete(socket, username, id);
		}
	});
});

function onclick_delete(socket, username, id){
	console.log('onclick_delete ', username, id);
	socket.emit('delete request', {'sender' : username, 'receiver' : id});
}

function onclick_accept(socket, username, id){
	console.log('onclick_accept ', username, id);
	socket.emit('accept request', {'sender' : username, 'receiver' : id});		
}

function onclick_send(socket, username, id){
	console.log('onclick_send ', username, id);
	socket.emit('send request', {'sender' : username, 'receiver' : id}); 
}
