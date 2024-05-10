from flask import Flask, request, jsonify
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from werkzeug.utils import secure_filename
import os
import io
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Global variables
dataset = None
X_train = None
X_test = None
y_train = None
y_test = None
classifier = None
best_classifier = None
best_accuracy = 0
best_classifier_name = None

@app.route('/api/upload', methods=['POST'])
def upload():
    global dataset
    file = request.files['file']
    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    return jsonify({'message': 'Dataset uploaded successfully'}), 200

@app.route('/api/preprocess', methods=['POST'])
def preprocess():
    global dataset, X_train, X_test, y_train, y_test
    dataset = dataset.values
    X = dataset[:,0:dataset.shape[1]-1]
    Y = dataset[:,dataset.shape[1]-1]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=0)
    return jsonify({'message': 'Dataset preprocessed', 'train_samples': len(X_train), 'test_samples': len(X_test)}), 200

@app.route('/api/train/lr', methods=['POST'])
def train_lr():
    global X_train, y_train, X_test, y_test, classifier, best_classifier,best_classifier_name, best_accuracy
    classifier = LogisticRegression()
    classifier.fit(X_train, y_train)
    predict = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predict) * 100
    precision = precision_score(y_test, predict, average='macro') * 100
    recall = recall_score(y_test, predict, average='macro') * 100
    f1 = f1_score(y_test, predict, average='macro') * 100

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_classifier = classifier
        best_classifier_name = 'Logistic Regression'

    return jsonify({'message': 'Logistic Regression model trained', 'accuracy_score': accuracy, 'precision_score': precision, 'recall_score': recall, 'f1_score': f1}), 200

@app.route('/api/train/dt', methods=['POST'])
def train_dt():
    global X_train, y_train, X_test, y_test, classifier, best_classifier, best_accuracy,best_classifier_name
    classifier = DecisionTreeClassifier(criterion = "entropy", splitter = "random", max_depth = 20,  min_samples_split = 50, min_samples_leaf = 20)
    classifier.fit(X_train, y_train)
    predict = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, predict) * 100
    precision = precision_score(y_test, predict, average='macro') * 100
    recall = recall_score(y_test, predict, average='macro') * 100
    f1 = f1_score(y_test, predict, average='macro') * 100

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_classifier = classifier
        best_classifier_name = 'Decision Tree'

    return jsonify({'message': 'Decision Tree model trained', 'accuracy_score': accuracy, 'precision_score': precision, 'recall_score': recall, 'f1_score': f1}), 200

@app.route('/api/predict', methods=['POST'])
def predict():
    global best_classifier, best_classifier_name
    file = request.files['file']
    test = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test.values

    predictions = best_classifier.predict(test_data)

    formatted_predictions = []
    for i, pred in enumerate(predictions):
        if pred == 0:
            formatted_predictions.append(f"{test_data[i]} Resources are available. Task can be scheduled\n")
        else:
            formatted_predictions.append(f"{test_data[i]} Resources are NOT available. Task can be scheduled after freeing resources\n")

    message = f'Prediction completed using {best_classifier_name}'
    return jsonify({'message': message, 'predictions': formatted_predictions}), 200
if __name__ == '__main__':
    app.run(debug=True)
