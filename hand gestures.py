import os
import numpy as np
import cv2
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# 1. Data Collection Function
# Capture video frames and label them with corresponding gesture
def collect_gesture_data(gesture_name, num_samples):
    cap = cv2.VideoCapture(0)
    data_dir = 'gesture_data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    gesture_dir = os.path.join(data_dir, gesture_name)
    if not os.path.exists(gesture_dir):
        os.makedirs(gesture_dir)

    print(f'Collecting {num_samples} samples for gesture "{gesture_name}"')
    count = 0
    while count < num_samples:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert to grayscale for simplicity
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Resize the frame to a fixed size
        resized_frame = cv2.resize(gray, (64, 64))

        # Show the frame
        cv2.imshow('Gesture Collection', frame)

        # Save frame to disk
        file_name = os.path.join(gesture_dir, f'{gesture_name}_{count}.jpg')
        cv2.imwrite(file_name, resized_frame)
        count += 1

        # Break if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Collected {count} frames for gesture {gesture_name}.")

# 2. Preprocessing the Dataset
def load_data(data_dir):
    images = []
    labels = []

    for gesture_name in os.listdir(data_dir):
        gesture_dir = os.path.join(data_dir, gesture_name)
        if not os.path.isdir(gesture_dir):
            continue

        for img_name in os.listdir(gesture_dir):
            img_path = os.path.join(gesture_dir, img_name)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = img / 255.0  # Normalize the image
            images.append(img)
            labels.append(gesture_name)

    images = np.array(images).reshape(-1, 64, 64, 1)  # Reshape for CNN
    label_encoder = LabelEncoder()
    labels = to_categorical(label_encoder.fit_transform(labels))

    return images, labels, label_encoder

# 3. CNN Model Definition
def build_model(input_shape, num_classes):
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D((2, 2)))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

# 4. Main Program
if __name__ == '__main__':
    gestures = ['play', 'pause', 'stop', 'volume_up', 'volume_down']
    num_samples_per_gesture = 500

    # Collecting gesture data
    for gesture in gestures:
        collect_gesture_data(gesture, num_samples_per_gesture)

    # Load and preprocess data
    data_dir = 'gesture_data'
    images, labels, label_encoder = load_data(data_dir)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

    # Build the CNN model
    input_shape = (64, 64, 1)  # Grayscale images, 64x64 pixels
    num_classes = len(gestures)
    model = build_model(input_shape, num_classes)

    # Train the model
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

    # Save the model
    model.save('gesture_recognition_cnn.h5')

    # Testing the model with live input
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray, (64, 64))
        reshaped_frame = np.expand_dims(resized_frame, axis=0).reshape(-1, 64, 64, 1)

        prediction = model.predict(reshaped_frame)
        predicted_class = np.argmax(prediction)
        gesture_label = label_encoder.inverse_transform([predicted_class])[0]

        cv2.putText(frame, gesture_label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
