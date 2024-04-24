from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pandas as pd
import io

app = Flask(__name__)
CORS(app)

@app.route('/api/train', methods=['POST'])
def train_models():
    # Read the data from request
    file = request.files['file']
    data = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    
    # Separate features and target
    X = data.drop('target_column', axis=1)
    y = data['target_column']
    
    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Logistic Regression model
    lr_model = LogisticRegression()
    lr_model.fit(X_train, y_train)
    
    # Train Random Forest model
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train, y_train)
    
    # Evaluate models
    lr_accuracy = accuracy_score(y_test, lr_model.predict(X_test))
    rf_accuracy = accuracy_score(y_test, rf_model.predict(X_test))
    
    # Return accuracy scores as JSON response
    return jsonify({
        'logistic_regression_accuracy': lr_accuracy,
        'random_forest_accuracy': rf_accuracy
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
