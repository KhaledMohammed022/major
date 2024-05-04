from flask import request, jsonify, send_file
import pandas as pd
import io
import logging
from flask import Flask
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

logging.basicConfig(level=logging.ERROR)

dataset = None
classifiers = {'lr': None, 'dt': None, 'rf': None}

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    global dataset
    file = request.files.get('file')

    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    dataset = dataset.dropna()
    return jsonify({'message': 'Dataset uploaded successfully'})

@app.route('/api/preprocess', methods=['POST'])
def preprocess_dataset():
    global dataset
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
    global classifiers
    if classifiers[model_name] is None:
        logging.error('Model not trained yet')
        return jsonify({'error': 'Model not trained yet'})

    predictions = classifiers[model_name].predict(test_data)
    return jsonify({'predictions': predictions.tolist()})

@app.route('/api/predict/lr', methods=['POST'])
def predict_lr():
    file = request.files.get('file')
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()
    return predict('lr', test_data)

@app.route('/api/predict/dt', methods=['POST'])
def predict_dt():
    file = request.files.get('file')
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()
    return predict('dt', test_data)

@app.route('/api/predict/rf', methods=['POST'])
def predict_rf():
    file = request.files.get('file')
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    try:
        test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
        test_data = test_data.dropna()

        predictions = classifiers['rf'].predict(test_data)

        result = []
        for i in range(len(predictions)):
            if predictions[i] == 0:
                result.append(f'Resources are available. Task can be scheduled: {test_data.iloc[i]}')
            else:
                result.append(f'Resources are NOT available. Task can be scheduled after freeing resources: {test_data.iloc[i]}')

        return jsonify({'predictions': result})
    except Exception as e:
        return jsonify({'error': str(e)})

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
