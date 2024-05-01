import logging
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import io
import matplotlib.pyplot as plt
import tempfile

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allowing all origins for demonstration purposes

# Configure logging to output to the console
logging.basicConfig(level=logging.ERROR)

# Global variables for dataset, classifiers, and feature names
dataset = None
classifiers = {'lr': None, 'dt': None, 'rf': None}
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

def train_model(model, model_name):
    global dataset, classifiers
    if dataset is None:
        logging.error('Dataset not uploaded or preprocessed yet')
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    model.fit(X_train, y_train)
    classifiers[model_name] = model

    predict = model.predict(X_test)
    acc = accuracy_score(y_test, predict) * 100
    p = precision_score(y_test, predict, average='macro') * 100
    r = recall_score(y_test, predict, average='macro') * 100
    f = f1_score(y_test, predict, average='macro') * 100

    return jsonify({
        'message': f'{model_name.capitalize()} model trained successfully',
        'accuracy_score': acc,
        'precision_score': p,
        'recall_score': r,
        'f1_score': f
    })

@app.route('/api/train/lr', methods=['POST'])
def train_lr():
    lr = LogisticRegression()
    return train_model(lr, 'lr')

@app.route('/api/train/dt', methods=['POST'])
def train_dt():
    dt = DecisionTreeClassifier(criterion='entropy', splitter='random', max_depth=20,
                                min_samples_split=50, min_samples_leaf=20)
    return train_model(dt, 'dt')

@app.route('/api/train/rf', methods=['POST'])
def train_rf():
    rf = RandomForestClassifier(n_estimators=10, criterion="entropy")
    return train_model(rf, 'rf')

def predict(model_name, test_data):
    global classifiers, feature_names
    if classifiers[model_name] is None:
        logging.error('Model not trained yet')
        return jsonify({'error': 'Model not trained yet'})

    # Check if the feature names in test data match those used during training
    if set(test_data.columns) != set(feature_names):
        logging.error('Feature names do not match')
        return jsonify({'error': 'Feature names do not match'})

    predictions = classifiers[model_name].predict(test_data)
    return jsonify({'predictions': predictions.tolist()})

@app.route('/api/predict/lr', methods=['POST'])
def predict_lr():
    file = request.files.get('file')  # Get the file from the request
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()  # Remove any rows with missing values
    return predict('lr', test_data)

@app.route('/api/predict/dt', methods=['POST'])
def predict_dt():
    file = request.files.get('file')  # Get the file from the request
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()  # Remove any rows with missing values
    return predict('dt', test_data)

@app.route('/api/predict/rf', methods=['POST'])
def predict_rf():
    file = request.files.get('file')  # Get the file from the request
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()  # Remove any rows with missing values
    return predict('rf', test_data)

def generate_plot(model_name, model):
    plt.figure(figsize=(8, 6))
    # Generate a plot specific to the model (for demonstration purposes)
    if model_name == 'lr':
        plt.plot([1, 2, 3, 4], [1, 4, 9, 16], label='Logistic Regression Plot')
    elif model_name == 'dt':
        plt.plot([1, 2, 3, 4], [1, 2, 4, 8], label='Decision Tree Plot')
    elif model_name == 'rf':
        plt.plot([1, 2, 3, 4], [2, 3, 5, 9], label='Random Forest Plot')

    plt.title(f'{model_name.upper()} Model Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.legend()
    
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(temp_file.name)
    plt.close()

    return send_file(temp_file.name, mimetype='image/png')

@app.route('/api/plot/lr', methods=['GET'])
def plot_lr():
    global classifiers
    return generate_plot('lr', classifiers['lr'])

@app.route('/api/plot/dt', methods=['GET'])
def plot_dt():
    global classifiers
    return generate_plot('dt', classifiers['dt'])

@app.route('/api/plot/rf', methods=['GET'])
def plot_rf():
    global classifiers
    return generate_plot('rf', classifiers['rf'])

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
