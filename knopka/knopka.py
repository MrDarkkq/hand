from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app, cors_allowed_origins="*")

current_state = "сжато"  # может быть "сжато" или "разжато"

# Конвертер для URL
url_map = {"compressed": "сжато", "expanded": "разжато"}

@app.route('/')
def index():
    state = request.args.get('state', '')
    if state in url_map:
        change_state(url_map[state])
    return render_template('index.html', state=current_state)

@app.route('/state/<state>')
def set_state(state):
    if state in url_map:
        change_state(url_map[state])
    return redirect('/')

def change_state(new_state):
    global current_state
    if new_state == current_state:
        return
    current_state = new_state
    socketio.emit('update', {'state': current_state})

@socketio.on('connect')
def connect():
    emit('update', {'state': current_state})

@socketio.on('switch')
def switch():
    new_state = "разжато" if current_state == "сжато" else "сжато"
    change_state(new_state)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)