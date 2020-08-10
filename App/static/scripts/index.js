document.addEventListener('DOMContentLoaded', function(){
	
	socket= io.connect('http://' + document.domain + ':' + location.port);
	username= document.getElementById('username').innerText.trim();
	
	socket.on('connect', function(){
		socket.send("Am I connected to you server?");
		socket.emit('join', {'name' : username});
	})
	socket.on('acknowledgement', (data) => {
		console.log("Server: ", data); 
		socket.emit('join', {'name': username});
	})
	socket.on('message', (msg)=> {
		console.log("Received: ", msg);
	})

	socket.on('request accepted', (data)=>{
		if(data['success']){
			alert(`${data['sender_name']} has accepted your friend request, refresh to start a conversation`);	
		}
	});

	socket.on('request deleted', (data)=>{
		if(data['success']){
			alert(`You are not friend with ${data['sender_name']} any more.`);	
		}
	})

	socket.on("new message response", (data)=>{
		console.log("in new message response", data['success']);

		if(data['success']){
			const message_text= document.getElementById('new_message_text');
			// console.log(message_text.value);
			add_messsage(
				{
					'message' : message_text.value,
					'sender' : null,
					'timestamp' : new Date().toString()
				}, data['receiver']
			)
			message_text.value= "";
			const friendcard= document.querySelector(`.friendcard[data-id="${data['receiver']}"]`)
			friendcard.querySelector('.last-message').textContent= 'you: ' + message_text.value;
		}
		
		else{
			alert("Something unexpected has occured pease refresh the page");
		}
	});

	socket.on('receive message', (data)=> {
		console.log(data);
		if(data['success']){
			const friendcard= document.querySelector(`.friendcard[data-id="${data['sender']}"]`);
			friendcard.querySelector('.last-message').textContent= data['message'];
			friendcard.querySelector('.lastseen').textContent= new Date(data['timestamp']).toLocaleString();
			if(document.getElementById('send') != null){
				// we are at receiver side
				if(document.getElementById('send').value == data['sender']){	
					add_messsage({
						'message' : data['message'],
						'sender' : data['sender'],
						'timestamp' : data['timestamp']
					}, data['sender']);

				}
			}			
		}
	})

	document.getElementById('logout').onclick= ()=>{
		socket.emit('leave', {'name' : username});
	}

	document.querySelectorAll('.friendcard').forEach( (friendcard) =>{
		let id= parseInt(friendcard.dataset.id);

		//don't know what
		last_seen= friendcard.querySelector('.lastseen').textContent;
		friendcard.querySelector('.lastseen').textContent= new Date(last_seen).toLocaleString();

		friendcard.addEventListener('click', ()=>{
			updateHeading(id);
			get_chat(id);
			document.getElementById('send').value= id;

			document.getElementById('send').onclick= ()=>{
				console.log("in onclick send");
				message_text= document.getElementById('new_message_text').value;
				payload= {
					'sender' : username,
					'receiver' : id,
					'message' : message_text
				};
				socket.emit('new message', payload);
			}
		}); 
	});
});

function updateHeading(id){
	const heading= document.getElementById('heading');
	const friendcard= document.querySelector(`.friendcard[data-id="${id}"]`);
	const src= friendcard.querySelector('img').src;
	const name= friendcard.querySelector('div.name').textContent;

	heading.textContent= "";

	image= document.createElement('img');
	image.src= src;
	image.classList.add('heading-image');

	heading_name= document.createElement('span');
	heading_name.textContent= name;
	heading_name.classList.add('heading-name');
	
	unfriend= document.createElement('button');
	unfriend.classList.add('unfriend-button');
	unfriend.textContent= "Unfriend";	
	unfriend.addEventListener('click', ()=>{
		const name= friendcard.querySelector('div.name').textContent.trim();
		confirm(`Are you sure you want to unfriend ${name}`);
		socket.emit('delete request', {'sender' : username, 'receiver' : id});
		location.reload();
	});

	heading.appendChild(image);
	heading.appendChild(heading_name);
	heading.appendChild(unfriend);	
	
	return heading;
}

function add_messsage(message_obj, id){

	message_card= document.createElement("div");
	message_card.classList.add("message_div");
	
	message_body= document.createElement("div");
	message_body.classList.add("message_body");
	message_body.innerHTML= message_obj['message'];

	moment= new Date(message_obj['timestamp']);
	stamp= moment.toLocaleString();
	message_stamp= document.createElement("div");
	message_stamp.classList.add("message_stamp");
	message_stamp.innerHTML= stamp;
	message_stamp.style.fontSize = 'smaller'

	message_card.appendChild(message_body);
	message_card.appendChild(message_stamp);

	if(message_obj['sender'] == id){
		message_card.style.marginRight = "auto";
		message_card.style.marginLeft = "10px";
		message_card.style.background = "yellow";
	}
	else{
		message_card.style.marginLeft = "auto";
		message_card.style.marginRight = "10px";
		message_card.style.background = "green";	
	}

	document.getElementById('chat_list').appendChild(message_card);
	updateScroll();
}

function updateScroll(){
    var element = document.getElementById("chat_list");
    element.scrollTop = element.scrollHeight;
}

function set_up_chat(chat, id){
	
	const img_div= document.getElementById('image_div');
	img_div.parentNode.removeChild(img_div);
	document.getElementById('chat_list').style.display= "flex";
	document.getElementById('chat_list').style.flexDirection = 'column';
	document.getElementById('chat_list').innerHTML= ''
	

	let form=document.getElementById('chat_form').style.display = "flex";
	document.getElementById('chat_form').style.marginTop= 'auto'

	for(i=0; i< chat.length; i++){
		add_messsage(chat[i], id);	
	}

	updateScroll();
}

function get_chat(id){

	xhr= new XMLHttpRequest();

	url= `/get_chat/id=${id}`;
	xhr.open('GET', url, true);
	xhr.onreadystatechange= function(){

		if(this.readyState == this.DONE && this.status == 200){
			response= JSON.parse(this.responseText);
			if(response.success === true){ 
				chat=  response.chat;
				set_up_chat(chat, id);
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

// function send_message(id){
// 		xhr= new XMLHttpRequest();

// 	url= "/send_message";
// 	id= parseInt(document.getElementById("send").value);
// 	message= document.getElementById("message_area").value;
// 	var params = `message=${message}&id=${id}`;

// 	xhr.open('POST', url, true);

// 	xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

// 	xhr.onreadystatechange= function(){
// 		if(this.readyState == this.DONE && this.status == 200){
// 			success= JSON.parse(this.responseText);
// 			if(success === true){ 
// 				get_chat(id);
// 				document.getElementById(`last_message_${id}`).innerHTML= `you: ${message}`	
// 			}
// 			else{
// 				alert(response.success);
// 			}
// 		}
// 		else if(this.status == 404){
// 			document.getElementById('about_me').innerHTML = 'Not Found';
// 		}
// 	}
// 	xhr.send(params);
// }