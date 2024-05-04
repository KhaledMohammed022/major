from flask import Flask, request, jsonify
import pandas as pd
import io
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

app = Flask(__name__)

# Global variables for dataset and trained models
dataset = None
lr_model = None
dt_model = None
rf_model = None
scaler = StandardScaler()  # Initialize a scaler

# Preprocessing function
def preprocess_data(data, fit_scaler=False):
    # Handle missing values (if any)
    data.dropna(inplace=True)
    
    # Perform encoding or scaling as needed
    # For example, encoding categorical variables
    data = pd.get_dummies(data)
    
    # Standardize numerical features
    numerical_cols = data.select_dtypes(include=['float64', 'int64']).columns
    if fit_scaler:  # Fit the scaler on the training data only
        scaler.fit(data[numerical_cols])
    data[numerical_cols] = scaler.transform(data[numerical_cols])  # Transform the data
    
    return data

# Endpoint for uploading dataset
@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    global dataset
    file = request.files.get('file')

    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded or empty filename'})

    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    
    return jsonify({'message': 'Dataset uploaded successfully'})

# Endpoint for preprocessing uploaded dataset
@app.route('/api/preprocess', methods=['POST'])
def preprocess_dataset():
    global dataset
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded yet'})

    dataset = preprocess_data(dataset, fit_scaler=True)
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    return jsonify({
        'message': 'Dataset preprocessed successfully',
        'train_samples': X_train.shape[0],
        'test_samples': X_test.shape[0
    })

# Endpoint for training Logistic Regression model
@app.route('/api/train/lr', methods=['POST'])
def train_lr():
    global dataset, lr_model
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    lr_model = LogisticRegression()
    lr_model.fit(X, y)

    return jsonify({'message': 'Logistic Regression model trained successfully'})

# Endpoint for training Decision Tree model
@app.route('/api/train/dt', methods=['POST'])
def train_dt():
    global dataset, dt_model
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    dt_model = DecisionTreeClassifier()
    dt_model.fit(X, y)

    return jsonify({'message': 'Decision Tree model trained successfully'})

# Endpoint for training Random Forest model
@app.route('/api/train/rf', methods=['POST'])
def train_rf():
    global dataset, rf_model
    if dataset is None:
        return jsonify({'error': 'Dataset not uploaded or preprocessed yet'})

    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]

    rf_model = RandomForestClassifier(n_estimators=100, random_state=0)
    rf_model.fit(X, y)

    return jsonify({'message': 'Random Forest model trained successfully'})

# Endpoint for predicting using Logistic Regression model
@app.route('/api/predict/lr', methods=['POST'])
def predict_lr():
    global lr_model
    if lr_model is None:
        return jsonify({'error': 'Logistic Regression model not trained yet'})

    test_data = pd.read_csv(io.StringIO(request.files['file'].read().decode('utf-8')))
    test_data = preprocess_data(test_data)
    predictions = lr_model.predict(test_data)

    return jsonify({'predictions': predictions.tolist()})

# Endpoint for predicting using Decision Tree model
@app.route('/api/predict/dt', methods=['POST'])
def predict_dt():
    global dt_model
    if dt_model is None:
        return jsonify({'error': 'Decision Tree model not trained yet'})

    test_data = pd.read_csv(io.StringIO(request.files['file'].read().decode('utf-8')))
    test_data = preprocess_data(test_data)
    predictions = dt_model.predict(test_data)

    return jsonify({'predictions': predictions.tolist()})

# Endpoint for predicting using Random Forest model
@app.route('/api/predict/rf', methods=['POST'])
def predict_rf():
    global rf_model
    if rf_model is None:
        return jsonify({'error': 'Random Forest model not trained yet'})

    test_data = pd.read_csv(io.StringIO(request.files['file'].read().decode('utf-8')))
    test_data = preprocess_data(test_data)
    predictions = rf_model.predict(test_data)

    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(debug=True)
