import sounddevice as sd
import numpy as np
import time
import sqlite3
import librosa
import io
from tensorflow import lite
import soundfile as sf
import requests
import speech_recognition as sr

def record_audio(duration=3, sample_rate=44100):
    print(f"Recording audio for {duration} seconds...")
    audio_data = sd.rec((duration*sample_rate), samplerate=sample_rate, channels=1, dtype=np.float32)
    print(sd.wait())
    print("Recording complete.")
    return audio_data.flatten()

def extract_mfccs(audio_data, sr):
    audio_data = librosa.util.normalize(audio_data)
    spectrogram = librosa.stft(audio_data)
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr,n_mfcc=20)  # Adjust n_mfcc as needed
    return mfccs # Transpose for common RNN input format

def ml_execute(data):
    interpreter = lite.Interpreter(model_path="my-lstm.tflite")
    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    interpreter.allocate_tensors()
    print(input_details)
    # output details
    print(output_details)
    interpreter.set_tensor(input_details[0]['index'], [data])
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

# Function to store audio data in the database
def store_audio_in_database(audio_data):
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recordings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            audio_data BLOB,
            command TEXT
        )
    ''')

    # Convert audio data to bytes
    audio_bytes = io.BytesIO()
    sf.write(audio_bytes, audio_data, 44100, format='WAV')

    # Insert audio data into the database
    cursor.execute('INSERT INTO recordings (audio_data) VALUES (?)', (audio_bytes.getvalue(),))
    connection.commit()

    # Close the connection
    connection.close()

# Function to retrieve audio data from the database
def retrieve_audio_from_database():
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()

    # Retrieve the latest recorded audio (you may need to adjust the query based on your requirements)
    cursor.execute('SELECT audio_data FROM recordings ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()

    # Close the connection
    connection.close()

    return result[0] if result else None

def add_result_todb(result):
    # Update the command column in the database
    connection = sqlite3.connect('your_database.db')
    cursor = connection.cursor()
   
    cursor.execute('UPDATE recordings SET command=? WHERE id=(SELECT MAX(id) FROM recordings)', (result,))
    connection.commit()
    connection.close()

if __name__ == "__main__":
    count=1
    while True:
        # Set the desired duration and sample rate
        recording_duration = 5

        # Record audio for the specified duration
        audio_data = record_audio(duration=recording_duration)

        # Now you can process or analyze the recorded audio data as needed
        print("Audio data shape:", audio_data.shape)
        wav_filename = "recorded_audio"+str(count)+".wav"
        count=count+1
        # sf.write(wav_filename, audio_data, 44100)
        store_audio_in_database(audio_data)

        print(f"Audio saved to {wav_filename}")

        # Example: Save the recorded audio to a WAV file
        data = extract_mfccs(audio_data, 44100)
        pad2d = lambda a, i: a[:, 0: i] if a.shape[1] > i else np.hstack((a, np.zeros((a.shape[0],i - a.shape[1]))))
        data=pad2d(data,40)
        data=data.astype(np.float32)
        print(data.shape)
        out=ml_execute(data)
        recognizer = sr.Recognizer()
        result1=""
        retrieved_audio_data = retrieve_audio_from_database()
        with sr.AudioFile(io.BytesIO(retrieved_audio_data)) as source:
            audio_datax = recognizer.record(source)
            try:
                result1 = recognizer.recognize_google(audio_datax)
            except:
                pass
        result=""
        if 'open' in result1:
            result='door_open'
        if 'close' in result1:
            result='door_close'
        if 'stop' in result1:
            result='door_stop'
        add_result_todb(result)
        percentage_list = []
        for i in range(len(out[0])):
            percentage_list.append("{0:.2%}".format(out[0][i]))
        classes=['door_open','door_close','door_stop']
        my_result = list(zip(classes, percentage_list))
        url = 'http://127.0.0.1:5000/update_data'
        data_to_send = {'audio_data_shape': audio_data.shape, 'mfcc_shape': data.shape, 'output': my_result, 'result' : result}
        response = requests.post(url, json=data_to_send)

        """print(f"Data sent to Flask application. Response: {response.json()}")"""

        time.sleep(5)
