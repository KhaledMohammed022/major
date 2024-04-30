from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
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

    lr = LogisticRegression()
    lr.fit(X, y)
    classifier = lr
    predict = dt.predict(X_test) 
    acc = accuracy_score(y_test,predict)*100
    p = precision_score(y_test,predict,average='macro') * 100
    r = recall_score(y_test,predict,average='macro') * 100
    f = f1_score(y_test,predict,average='macro') * 100
    return jsonify({'message': 'Logistic Regression model trained successfully'})
    precision.append(p)
    accuracy.append(acc)
    recall.append(r)
    fscore.append(f)
    return jsonify({'message': 'Accuracy Score : '})
    return jsonify({'message': 'Logistics Regression Precision : '})
    return jsonify({'message': 'Logistics Regression Recall : '})
    return jsonify({'message': 'Logistics Regression F1 Score : '})

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
    predict = dt.predict(X_test) 
    acc = accuracy_score(y_test,predict)*100
    p = precision_score(y_test,predict,average='macro') * 100
    r = recall_score(y_test,predict,average='macro') * 100
    f = f1_score(y_test,predict,average='macro') * 100
    return jsonify({'message': 'Decision Tree model trained successfully'})
    precision.append(p)
    accuracy.append(acc)
    recall.append(r)
    fscore.append(f)
    return jsonify({'message': 'Accuracy Score : '})
    return jsonify({'message': 'Decision Tree Precision : '})
    return jsonify({'message': 'Decision Tree Recall : '})
    return jsonify({'message': 'Decision Tree F1 Score : '})

    

@app.route('/api/predict', methods=['POST'])

def predict():
    text.delete('1.0', END)
    global classifier
    filename = filedialog.askopenfilename(initialdir="Dataset")
    test = pd.read_csv(filename)
    test = test.values
    predict = classifier.predict(test)
    print(predict)
    for i in range(len(predict)):
        if predict[i] == 0:
            text.insert(END,str(test[i])+" Resources are available. Task can be schedule\n\n")
        else:
            text.insert(END,str(test[i])+" Resources are NOT available. Task can be schedule after freeing resources\n\n")
