import sqlite3
from flask import Flask, render_template, redirect, jsonify, request, url_for
from flask_socketio import SocketIO, emit
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

import datetime

# Todo: add nice error page 
# Todo: add direct login after register

app = Flask(__name__)
app.secret_key = "secret key"
socketio = SocketIO(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin):
  def __init__(self, id, username):
    self.id = id
    self.username = username

# Load user from session
@login_manager.user_loader
def load_user(user_id):
  """This function loads the user object based on id(username)."""
  with sqlite3.connect('chat.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT id, username FROM users WHERE id = ?', (user_id))
    user = cursor.fetchall()[0] # returns a tuple
    
  if user:
    return User(user[0], user[1])
  return None


# render the chat home page
@app.route("/")
def home():
  return render_template('index.html')

@app.route("/register", methods=["GET","POST"])
def register():
  # check if user made post request
  if request.method == "POST":
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
      return jsonify({'error': 'username and passwor are required'}), 400
    
    hashed_password = generate_password_hash(password)

    try:
      with sqlite3.connect('chat.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        return redirect(url_for('login'))
    except sqlite3.IntegrityError:
      return jsonify({'message': 'Username Already exists'}), 400
    except Exception as e:
      return jsonify({'message': f'[ERROR] {e}'}), 400

  return render_template('register.html')


@app.route("/login", methods=["GET","POST"])
def login():
  # if request == post then find user in database
  if request.method == "POST":
    data = request.form
    username = data.get('username')
    password = data.get('password')
    try:

      with sqlite3.connect('chat.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password FROM users WHERE username = ?', (username,))# or use list literal [username]
        user = cursor.fetchall()[0]# returns tuple inside a list
    except Exception as e:
      return jsonify({'message': 'user does not exist'})
    if user and check_password_hash(user[2], password):
      user_obj = User(user[0], user[1])
      login_user(user_obj)
      return redirect(url_for('home'))
    return jsonify({'message': ' Invalid credentials'}), 401
  return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
  logout_user()
  return redirect(url_for('home'))


# Route to fetch all messages
@app.route("/api/messages", methods=["GET"])
@login_required
def get_messages():
  conn = sqlite3.connect('chat.db')
  cursor = conn.cursor()

  # Fetch all messages
  cursor.execute("SELECT username, content, timestamp FROM messages ORDER by timestamp ASC")
  messages = cursor.fetchall()
  conn.close()

  # format message before returning
  formated_message = [
    {'username': msg[0], 
     'content': msg[1], 
     'timestamp': datetime.datetime.strptime(msg[2], '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
     }
    for msg in messages
  ] 
  return jsonify(formated_message)

@app.route("/api/messages", methods=["POST"])
def add_message():
  data = request.json # get JSON data from the request
  username = current_user.username
  content = data.get('content')
  # validate inputs
  if not username or not content:
    return jsonify({'error': 'inavlid input'}), 400
  
  with sqlite3.connect('chat.db') as conn:
    cursor = conn.cursor()
    # insert new messages into database
    cursor.execute('INSERT INTO messages (username, content) VALUES (?, ?)', (username, content))
    conn.commit()
    cursor.execute('SELECT username, timestamp FROM messages WHERE username = ?',(username,))
    time = cursor.fetchall()[0][1]
  
  timestamp = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S').strftime('%H:%M:%S')
  socketio.emit('new_message', {"username": username, "content": content, 'timestamp': timestamp})

  return jsonify({'message': 'message added seccesfully!'}), 201 

@socketio.on('connect')
def handle_connect():
  if not current_user.is_authenticated:
    return False # deny connection
  emit('notification', {'message': f'{current_user.username} has joined the chat'}, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
  if current_user.is_authenticated:
   emit('notification', {'message': f'{current_user.username} left the chat'}, broadcast=True)

if __name__ == "__main__":
  socketio.run(app, debug=True)