import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import io

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allowing all origins for demonstration purposes

# Configure logging to output to the console
logging.basicConfig(level=logging.ERROR)

# Global variables for dataset, classifier, and evaluation metrics
dataset = None
classifier = None
feature_names = None  # To store feature names from the training data

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    global dataset, feature_names
    file = request.files.get('file')  # Get the file from the request

    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    dataset = dataset.dropna()  # Remove any rows with missing values
    feature_names = list(dataset.columns)[:-1]  # Exclude the target column
    return jsonify({'message': 'Dataset uploaded successfully'})

@app.route('/api/preprocess', methods=['POST'])
def preprocess_dataset():
    global dataset, feature_names
    if dataset is None:
        logging.error('Dataset not uploaded yet')
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
    global dataset, classifier, feature_names
    if dataset is None:
        logging.error('Dataset not uploaded or preprocessed yet')
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    classifier = lr

    predict = lr.predict(X_test)
    acc = accuracy_score(y_test, predict) * 100
    p = precision_score(y_test, predict, average='macro') * 100
    r = recall_score(y_test, predict, average='macro') * 100
    f = f1_score(y_test, predict, average='macro') * 100

    return jsonify({
        'message': 'Logistic Regression model trained successfully',
        'accuracy_score': acc,
        'precision_score': p,
        'recall_score': r,
        'f1_score': f
    })

@app.route('/api/train/dt', methods=['POST'])
def train_dt():
    global dataset, classifier, feature_names
    if dataset is None:
        logging.error('Dataset not uploaded or preprocessed yet')
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    dt = DecisionTreeClassifier(criterion='entropy', splitter='random', max_depth=20,
                                min_samples_split=50, min_samples_leaf=20)
    dt.fit(X_train, y_train)
    classifier = dt

    predict = dt.predict(X_test)
    acc = accuracy_score(y_test, predict) * 100
    p = precision_score(y_test, predict, average='macro') * 100
    r = recall_score(y_test, predict, average='macro') * 100
    f = f1_score(y_test, predict, average='macro') * 100

    return jsonify({
        'message': 'Decision Tree model trained successfully',
        'accuracy_score': acc,
        'precision_score': p,
        'recall_score': r,
        'f1_score': f
    })

@app.route('/api/train/rf', methods=['POST'])
def train_rf():
    global dataset, classifier, feature_names
    if dataset is None:
        logging.error('Dataset not uploaded or preprocessed yet')
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    rf = RandomForestClassifier(n_estimators=10, criterion="entropy")
    rf.fit(X_train, y_train)
    classifier = rf

    predict = rf.predict(X_test)
    acc = accuracy_score(y_test, predict) * 100
    p = precision_score(y_test, predict, average='macro') * 100
    r = recall_score(y_test, predict, average='macro') * 100
    f = f1_score(y_test, predict, average='macro') * 100

    return jsonify({
        'message': 'Random Forest model trained successfully',
        'accuracy_score': acc,
        'precision_score': p,
        'recall_score': r,
        'f1_score': f
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    global classifier, feature_names
    if classifier is None:
        logging.error('Model not trained yet')
        return jsonify({'error': 'Model not trained yet'})

    file = request.files.get('file')  # Get the file from the request
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()  # Remove any rows with missing values

    if set(test_data.columns) != set(feature_names):
        logging.error('Feature names do not match')
        return jsonify({'error': 'Feature names do not match'})

    predictions = classifier.predict(test_data)

    return jsonify({'predictions': predictions.tolist()})

# Error handling for 404 (Not Found) and 500 (Internal Server Error)
@app.errorhandler(404)
def not_found_error(error):
    logging.error('Not Found: %s', request.url)
    return jsonify({'error': 'Not Found'}), 404

@app.errorhandler(500)
def internal_error(error):
    logging.error('Internal Server Error: %s', error)
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
