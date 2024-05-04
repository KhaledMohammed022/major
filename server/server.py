import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import io

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allowing all origins for demonstration purposes

# Configure logging to output to the console
logging.basicConfig(level=logging.ERROR)

# Global variable for the classifier
classifier = None

@app.route('/api/train/rf', methods=['POST'])
def train_rf():
    global classifier
    if classifier is not None:
        logging.error('Model already trained')
        return jsonify({'error': 'Model already trained'})

    file = request.files.get('file')  # Get the file from the request
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    dataset = dataset.dropna()  # Remove any rows with missing values

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    # Train the Random Forest classifier
    classifier = RandomForestClassifier(n_estimators=10, criterion="entropy")
    classifier.fit(X, y)

    return jsonify({'message': 'Random Forest classifier trained successfully'})

@app.route('/api/predict/rf', methods=['POST'])
def predict_rf():
    global classifier
    if classifier is None:
        logging.error('Model not trained yet')
        return jsonify({'error': 'Model not trained yet'})

    file = request.files.get('file')  # Get the file from the request
    if not file or file.filename == '':
        logging.error('No file uploaded or empty filename')
        return jsonify({'error': 'No file uploaded or empty filename'})

    test_data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    test_data = test_data.dropna()  # Remove any rows with missing values

    # Perform prediction using the trained classifier
    predictions = classifier.predict(test_data)

    # Format the predictions for response
    prediction_results = []
    for i in range(len(predictions)):
        if predictions[i] == 0:
            prediction_results.append(f"Resources are available for {test_data.iloc[i]}")
        else:
            prediction_results.append(f"Resources are NOT available for {test_data.iloc[i]}")

    return jsonify({'predictions': prediction_results})

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
