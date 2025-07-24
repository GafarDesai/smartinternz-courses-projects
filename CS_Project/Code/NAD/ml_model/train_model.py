import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib

# Load the data
data_path = 'network_traffic.csv'  # Ensure this CSV file has new or combined data
data = pd.read_csv(data_path)

# Encode categorical columns
label_encoders = {}
for col in ['protocol', 'flag', 'source_ip', 'destination_ip']:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col].astype(str))
    label_encoders[col] = le

# Features and target
X = data.drop(columns=['timestamp', 'is_anomaly'])  # Drop timestamp and label
y = data['is_anomaly']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Ensure ml_model folder exists
os.makedirs('ml_model', exist_ok=True)

# Save model and encoders
joblib.dump(clf, 'ml_model/anomaly_detector.pkl')
joblib.dump(label_encoders, 'ml_model/label_encoders.pkl')

print("✅ Model retrained and saved successfully!")
