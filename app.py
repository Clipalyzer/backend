from flask import Flask, render_template
from flask_socketio import SocketIO
import pytesseract
from grab_images_from_video import grab_all_images

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
video_path = "G:\Videos\Valorant"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode='gevent')

if __name__ == '__main__':
    socketio.run(app)

@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/generate_initial")
def generate_initial():
    grab_all_images(video_path)
    return "ok"