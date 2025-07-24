from predict_route import register_predict_route
from flask import Flask, render_template
from flask_cors import CORS
import os
from flask import Flask, request, jsonify, render_template  # add render_template if not imported
import pandas as pd
import joblib
from sklearn.linear_model import LogisticRegression  # or your actual model

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, '../templates')
STATIC_DIR = os.path.join(BASE_DIR, '../static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

# Register /predict route from separate file
register_predict_route(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if __name__ == '__main__':
    app.run(debug=True)
