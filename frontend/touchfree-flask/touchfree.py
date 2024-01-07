from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import speech_recognition as sr
from threading import Thread
import time

app = Flask(__name__)
socketio = SocketIO(app)

captured_text = ""
trigger_word = "link"  # Replace with your trigger word


class SpeechListener(Thread):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def run(self):
        with self.microphone as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            last_update_time = 0
            while True:
                try:
                    audio_data = self.recognizer.listen(source, timeout=3)
                    text = self.recognizer.recognize_google(audio_data).lower()
                    print("Heard:", text)
                    if time.time() - last_update_time > 2:  # Update every 2 seconds
                        socketio.emit('captured_text', {'text': text})
                        last_update_time = time.time()
                    
                    if trigger_word.lower() in text:
                        self.callback(text.replace("link",""))
                except sr.UnknownValueError:
                    print("nothing")
                    pass  # Ignore if speech is not recognized
                except sr.RequestError as e:
                    print("Speech Recognition error:", str(e))

listener_thread = SpeechListener(callback=lambda text: socketio.emit('captured_text', {'text': text}))
listener_thread.daemon = True
listener_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)
