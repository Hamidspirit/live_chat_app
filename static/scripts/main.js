const socket = io(); //initilize web socket connection

// listen for new messages
socket.on('new_message',  (data)=>{
    const messagesDiv = document.getElementById("messages");
    const messageElement = document.createElement("div");
    
    messageElement.classList.add("messages");
    const avatarUrl = `https://api.dicebear.com/9.x/pixel-art/svg?seed=${data.username}`;
        messageElement.innerHTML = `
        <img src="${avatarUrl}" class="avatar" alt="Avatar">
        <strong>${data.username}</strong>: ${data.content} <small>[${data.timestamp}]</small>
    `;
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
        messageElement.classList.add('messages');
        const avatarUrl = `https://api.dicebear.com/9.x/pixel-art/svg?seed=${msg.username}`;
         messageElement.innerHTML = `
            <img src="${avatarUrl}" class="avatar" alt="Avatar">
            <strong>${msg.username}</strong>: ${msg.content} <small>[${msg.timestamp}]</small>
        `;
        messagesDiv.appendChild(messageElement);
    });
}

loadMessages(); // initial load 