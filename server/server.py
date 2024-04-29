from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
import io
import numpy as np

app = Flask(__name__)
CORS(app)

# Global variables for dataset and classifier
dataset = None
classifier = None

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    global dataset
    file = request.files.get('file')  # Get the file from the request

    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded or empty filename'})

    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    dataset = dataset.dropna()  # Remove any rows with missing values
    return jsonify({'message': 'Dataset uploaded successfully'})

@app.route('/api/preprocess', methods=['POST'])
def preprocess_dataset():
    global dataset
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    return jsonify({
        'message': 'Dataset preprocessed successfully',
        'train_samples': X_train.shape[0],
        'test_samples': X_test.shape[0]
    })

@app.route('/api/train/lr', methods=['POST'])
def train_lr():
    global dataset, classifier
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    lr = LogisticRegression()
    lr.fit(X, y)
    classifier = lr

    return jsonify({'message': 'Logistic Regression model trained successfully'})

@app.route('/api/train/dt', methods=['POST'])
def train_dt():
    global dataset, classifier
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    dt = DecisionTreeClassifier(criterion='entropy', splitter='random', max_depth=20,
                                min_samples_split=50, min_samples_leaf=20)
    dt.fit(X, y)
    classifier = dt

    return jsonify({'message': 'Decision Tree model trained successfully'})

@app.route('/api/predict', methods=['POST'])
def predict():
    global classifier
    if classifier is None:
        return jsonify({'error': 'Model not trained yet'})

    file = request.files.get('file')
    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    predictions = classifier.predict(test_data)

    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True, port=8080)
