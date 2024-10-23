# Import necessary libraries
# Import necessary libraries for Flask API
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# Load dataset (use a local CSV file or download from UCI repository)
# Here we assume the dataset is heart.csv
data = pd.read_csv("heart.csv")

# Inspect dataset
print(data.head())

# Data preprocessing
# Separating features and target
X = data.drop(columns=['target'])  # Features (exclude the label column)
y = data['target']  # Labels (target column)

# Split dataset into training and testing set (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the feature set
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Model: Logistic Regression (simple model)
model = LogisticRegression()

# Train the model
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))

# Print confusion matrix and classification report
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Save the trained model and scaler using joblib for later use in deployment
import joblib
joblib.dump(model, 'health_diagnosis_model.pkl')
joblib.dump(scaler, 'scaler.pkl')


# Initialize Flask app
app = Flask(__name__)

# Load the trained model and scaler
model = joblib.load('health_diagnosis_model.pkl')
scaler = joblib.load('scaler.pkl')

# Define a route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the JSON input from the user (as features)
        data = request.json
        features = np.array([data['age'], data['sex'], data['cp'], data['trestbps'], 
                             data['chol'], data['fbs'], data['restecg'], data['thalach'], 
                             data['exang'], data['oldpeak'], data['slope'], data['ca'], 
                             data['thal']])

        # Preprocess the input (scale it)
        scaled_features = scaler.transform([features])

        # Predict using the loaded model
        prediction = model.predict(scaled_features)[0]

        # Return the prediction result (1 = Disease, 0 = No Disease)
        result = 'Disease' if prediction == 1 else 'No Disease'
        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)})

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
