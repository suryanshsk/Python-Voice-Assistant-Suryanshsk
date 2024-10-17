from flask import Flask, request, jsonify
import librosa
import torch
import os
from speechbrain.pretrained import EncoderClassifier
from pydub import AudioSegment

app = Flask(__name__)

# Load the pre-trained model (using SpeechBrain pre-trained model)
classifier = EncoderClassifier.from_hparams(source="speechbrain/emotion-recognition", savedir="tmp")

# Function to process audio and extract emotion
def predict_emotion(file_path):
    try:
        # Load audio file
        signal, sample_rate = librosa.load(file_path, sr=16000)
        
        # Convert to a Torch tensor
        signal_tensor = torch.tensor(signal).unsqueeze(0)
        
        # Predict emotions
        emotion_prediction = classifier.classify_batch(signal_tensor)
        
        # Extract emotion label (predicted emotion class)
        emotion = emotion_prediction[3][0]
        return emotion
    
    except Exception as e:
        return str(e)

# Route to upload and detect emotion from voice file
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    # Save the file
    filename = file.filename
    file_path = os.path.join('uploads', filename)
    
    # Convert file to WAV format if it's not in WAV format
    if filename.endswith('.mp3'):
        audio = AudioSegment.from_mp3(file)
        file_path = os.path.join('uploads', filename.replace('.mp3', '.wav'))
        audio.export(file_path, format='wav')
    else:
        file.save(file_path)
    
    # Predict emotion from audio
    emotion = predict_emotion(file_path)
    
    return jsonify({"emotion": emotion})

if __name__ == '__main__':
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)
