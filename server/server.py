from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import io

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allowing all origins for demonstration purposes

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
    global dataset, classifier
    if dataset is None:
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

@app.route('/api/predict', methods=['POST'])
def predict():
    global classifier
    file = request.files.get('file')  # Get the file from the request

    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded or empty filename'})

    # Assuming the uploaded file is a CSV file
    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()  # Remove any rows with missing values

    # Perform any necessary preprocessing on the test data
    # For example, if the test data has the same features as the training data,
    # you can directly use the classifier to make predictions
    predictions = classifier.predict(test_data)

    # Assuming predictions is a list of predicted labels or classes
    # You can format the predictions as needed and return them in the response
    return jsonify({'predictions': predictions})

if __name__ == '__main__':
    app.run(debug=False)
