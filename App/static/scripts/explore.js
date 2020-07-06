document.addEventListener('DOMContentLoaded', function(){
	let users= document.querySelectorAll('.user_detail_upper');
	for(let i= 0; i < users.length; i++){

		let button = document.createElement("button");
		button.innerHTML = "send request";

		button.addEventListener ("click", function() {
  			alert("did something");
		});
		button.classList.add("user_button");
		users[i].appendChild(button);
	}
});