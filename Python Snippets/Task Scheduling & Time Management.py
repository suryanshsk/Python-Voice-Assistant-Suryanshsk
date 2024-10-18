import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset (assumed to be a CSV file)
# Example dataset can be downloaded from Kaggle, for example, "Task Completion Prediction"
# Replace the path with your local dataset file
df = pd.read_csv('tasks_dataset.csv')

# Assume the dataset has columns: urgency, importance, deadline_hours_left, task_length_hours, priority
# Preview the dataset to understand its structure
print(df.head())

# Features and labels (adjust based on actual column names from the dataset)
X = df[['urgency', 'importance', 'deadline_hours_left', 'task_length_hours']]  # Features
y = df['priority']  # Priority labels (1 for high priority, 0 for low)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize the Random Forest Classifier
clf = RandomForestClassifier()

# Train the model
clf.fit(X_train, y_train)

# Predict priorities for the test set
y_pred = clf.predict(X_test)

# Calculate and print the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Test the model with a new task (provide actual values for urgency, importance, etc.)
new_task = [[4, 5, 8, 2]]  # Example: [urgency, importance, deadline_hours_left, task_length_hours]
predicted_priority = clf.predict(new_task)
print(f'Predicted priority for the new task: {"High" if predicted_priority[0] == 1 else "Low"}')

# Feature importance to understand how the model prioritizes tasks
feature_importances = clf.feature_importances_
for feature, importance in zip(X.columns, feature_importances):
    print(f'Feature: {feature}, Importance: {importance}')
