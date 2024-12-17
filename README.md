# About Chat App
A real-time live chat application built using Flask as the backend, SQLite as the database, and HTML, CSS, and JavaScript for the frontend. The app features user authentication, and real-time communication via WebSockets (using Flask-SocketIO).


## Features
1. User Authentication
    * Secure login and registration using Flask-Login.
    * Passwords hashed using werkzeug.security for security.
2. Real-Time Messaging
    * Users can send and receive messages instantly via WebSockets.
3. SQLite Database

4. Secure WebSocket Connections

# Installation
Prerequisites: 
Ensure you have Python 3.8+ and pip installed on your system.

Move to a preferred directory

* Step 1: Clone the Repository
```bash 
git clone https://github.com/hamidspirit/live_chat_app.git
```
```bash
cd flask-live-chat
```

* Step 2: Create a Virtual Environment
```bash
python -m venv venv
```
```bash
source venv/bin/activate  
```

on windows
```bash
venv\Scripts\activate
```
* Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

* Step 4: Initialize the Database
```bash
python models.py
```
The database file chat.db will be created automatically.

# Run the App
* Start flask server
```bash
python app.py
```

Open your browser and go to:
 > http://127.0.0.1:5000