import json
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO
import pytesseract
from queue import Queue
from generator import (
    generate_file_system,
    grab_images_from_video,
    grab_detailed_images_from_video,
    generate_testing_images,
    create_configs,
)

# from grab_images_from_video import grab_all_images

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
video_path = "G:\Videos\Valorant"

generate_file_system()
q = Queue()

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app, async_mode="gevent")

if __name__ == "__main__":
    socketio.run(app)

# A thread that consumes data
def consumer(in_q):
    while True:
        data = in_q.get()
        print(data)
        socketio.emit("update", json.dumps(data))


@socketio.on("message")
def handle_message(data):
    print("received message: " + data)


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/generate_initial")
def generate_initial():
    q.put({"thread": 1, "current": 1, "max": len([]), "file_name": "file_name"})
    # grab_images_from_video(video_path, q)
    return "ok"


t1 = Thread(target=consumer, args=(q,))
t1.start()
