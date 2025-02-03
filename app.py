from flask import Flask, request, jsonify
import pandas as pd
import joblib
import numpy as np

# Load the trained model and scaler
model = joblib.load("customer_segmentation.pkl")
scaler = joblib.load("scaler.pkl")

# Load the dataset used during training to get correct feature names
df_original = pd.read_csv('E-commerce Customer Behavior.csv')

# Convert categorical variables the same way as in training
df_original["Gender"] = df_original["Gender"].map({"Male": 0, "Female": 1})
df_original = pd.get_dummies(df_original, columns=["City", "Membership Type", "Satisfaction Level"], drop_first=False)

# Drop Customer ID if it exists
df_original.drop(columns=["Customer ID"], inplace=True, errors='ignore')

# Get the exact feature names used during model training
required_columns = df_original.columns.tolist()

# Define customer segment labels
cluster_labels = {
    0: "Casual Buyers",
    1: "High Spenders",
    2: "Frequent Shoppers",
    3: "Infrequent Buyers"
}

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Customer Segmentation API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input
        data = request.json
        
        # Convert input to DataFrame
        df_input = pd.DataFrame([data])

        # Ensure input has the same features as training data
        for col in required_columns:
            if col not in df_input.columns:
                df_input[col] = 0  # Fill missing columns with 0

        # Ensure columns are in the same order
        df_input = df_input[required_columns]

        # Scale input data
        df_scaled = scaler.transform(df_input)

        # Predict cluster
        cluster = model.predict(df_scaled)[0]

        # Get customer segment label
        segment = cluster_labels.get(cluster, "Unknown Segment")

        return jsonify({"Predicted Cluster": int(cluster), "Customer Segment": segment})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run Flask app
if __name__ == "__main__":
    app.run(debug=True)