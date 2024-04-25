from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import pandas as pd
import io
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)

# Global variables for dataset and classifier
dataset = None
classifier = None

@app.route('/api/upload', methods=['POST'])
def upload_dataset():
    global dataset, classifier
    file = request.files.get('file')  # Get the file from the request

    if not file or file.filename == '':
        return jsonify({'error': 'No file uploaded or empty filename'})

    dataset = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    dataset = dataset.values
    X = dataset[:, 0:dataset.shape[1] - 1]
    y = dataset[:, dataset.shape[1] - 1]

    indices = np.arange(X.shape[0])
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    lr = LogisticRegression()
    lr.fit(X_train, y_train)
    classifier = lr

    dt = DecisionTreeClassifier(criterion='entropy', splitter='random', max_depth=20,
                                 min_samples_split=50, min_samples_leaf=20)
    dt.fit(X_train, y_train)

    predictions_lr = lr.predict(X_test)
    predictions_dt = dt.predict(X_test)

    accuracy_lr = accuracy_score(y_test, predictions_lr)
    accuracy_dt = accuracy_score(y_test, predictions_dt)

    return jsonify({
        'message': 'Dataset uploaded and processed successfully',
        'train_samples': X_train.shape[0],
        'test_samples': X_test.shape[0],
        'lr_accuracy': accuracy_lr,
        'dt_accuracy': accuracy_dt
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
