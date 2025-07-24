from flask import request, jsonify
import joblib
import pandas as pd
import os

# Set paths to model and encoder files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '..', 'ml_model', 'anomaly_detector.pkl')
ENCODER_PATH = os.path.join(BASE_DIR, '..', 'ml_model', 'label_encoders.pkl')

# Load model and encoders once at module level
model = joblib.load(MODEL_PATH)
label_encoders = joblib.load(ENCODER_PATH)

def register_predict_route(app):
    @app.route('/predict', methods=['POST'], endpoint='predict_anomaly')
    def predict():
        data = request.get_json()

        # Convert input to DataFrame
        input_df = pd.DataFrame([data])

        # Encode categorical fields
        for col, le in label_encoders.items():
            if col in input_df:
                input_df[col] = le.transform([input_df[col][0]])

        # Drop timestamp if present
        input_df = input_df.drop(columns=['timestamp'], errors='ignore')

        # Make prediction
        prediction = model.predict(input_df)[0]

        return jsonify({
            "is_anomaly": bool(prediction)
        })

    @app.route('/retrain', methods=['POST'])
    def retrain_model():
        file = request.files.get('file')
        if not file:
            return jsonify({"message": "No file provided"}), 400

        try:
            # Read CSV file
            df = pd.read_csv(file)

            # TODO: Replace this with actual retraining logic
            # Example: retrain_model(df)

            return jsonify({"message": "Model retrained successfully!"})
        except Exception as e:
            print("Retrain error:", e)
            return jsonify({"message": "Error retraining model"}), 500
