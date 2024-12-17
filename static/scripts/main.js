const socket = io(); //initilize web socket connection

// listen for new messages
socket.on('new_message',  (data)=>{
    const messagesDiv = document.getElementById("messages");
    const messageElement = document.createElement("div");

    messageElement.innerHTML = stylingMessages(data, messageElement) 
    messagesDiv.appendChild(messageElement);

    // scrol to bottom
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

socket.on('notification', (data)=>{
    const messageDiv = document.getElementById('messages');
    const notificationElement = document.createElement("div");
    notificationElement.classList.add('notification');
    notificationElement.textContent = data.message;
    messageDiv.appendChild(notificationElement);

    // scroll to bottom
    messageDiv.scrollTop = messageDiv.scrollHeight;
})

document.getElementById('message_form').addEventListener('submit', async (event) => {
    event.preventDefault(); // prevent the form from refreshing the page

    // const username = document.getElementById('username').value.trim();
    const message = document.getElementById('message').value.trim();

    if(!message){
        alert('message is required!')
        return;
    }

    // send message to the server
    const response = await fetch('/api/messages', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({content: message})
    })

    if(response.ok){
        document.getElementById('message').value = ''; // clear message input
    }else {
        alert("failed to send the messages. try again.")
    }
})

// fetch and display  messages 
async function loadMessages(){
    const response = await fetch('/api/messages');
    const messages = await response.json();

    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML = ''; // clear old messages

    messages.forEach(msg => {
        const messageElement = document.createElement("div");
        // messageElement.classList.add('messages');
        messageElement.innerHTML = stylingMessages(msg, messageElement)
        messagesDiv.appendChild(messageElement);
    });
}

loadMessages(); // initial load 

function stylingMessages(data, messageElement){
    // add diferent style for active client 
    const currentUser = document.getElementById("user").innerText.slice(6);
    if(currentUser === data.username){
        messageElement.classList.add("current_user_message")
    }else{
        messageElement.classList.add("messages");
    }
    // add profile pic and styling to message div
    const avatarUrl = `https://api.dicebear.com/9.x/pixel-art/svg?seed=${data.username}`;
    inlineStyle = `
    <img src="${avatarUrl}" class="avatar" alt="Avatar">
    <strong>${data.username}</strong> ${data.content} <small>[${data.timestamp}]</small `;
    return inlineStyle
}