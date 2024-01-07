from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

current_data = {'output':[]}  # Store the latest received data globally

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_data', methods=['POST'])
def update_data():
    global current_data
    data = request.get_json()
    
    # Process the received data as needed
    current_data = {
        'audio_data_shape': data.get('audio_data_shape', ()),
        'mfcc_shape': data.get('mfcc_shape', ()),
        'output': data.get('output', []),
        'result' : data.get('result',[])
    }
    return jsonify(success=True)

@app.route('/get_current_data')
def get_current_data():
    global current_data
    print(current_data)
    return jsonify(current_data)

if __name__ == '__main__':
    app.run(debug=True)
