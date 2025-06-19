# app.py
# This script creates a Flask web API to serve the employee attrition prediction model,
# now including a basic web form for user-friendly input.

from flask import Flask, request, jsonify, render_template_string
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# --- Load Saved Model and Scaler ---
print("--- Loading saved model and scaler ---")
try:
    model = pickle.load(open("model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
    print("Model and Scaler loaded successfully!")
except FileNotFoundError:
    print("Error: 'model.pkl' or 'scaler.pkl' not found.")
    print("Please ensure you have run 'model_dev.py' successfully to create these files in the same folder.")
    model = None
    scaler = None
except Exception as e:
    print(f"An unexpected error occurred while loading model/scaler: {e}")
    model = None
    scaler = None

# --- Define expected feature names ---
expected_features_order = ['Age', 'DailyRate', 'DistanceFromHome', 'Education', 'EnvironmentSatisfaction',
                           'HourlyRate', 'JobInvolvement', 'JobLevel', 'JobSatisfaction', 'MonthlyIncome',
                           'MonthlyRate', 'NumCompaniesWorked', 'PercentSalaryHike', 'PerformanceRating',
                           'RelationshipSatisfaction', 'StockOptionLevel', 'TotalWorkingYears',
                           'TrainingTimesLastYear', 'WorkLifeBalance', 'YearsAtCompany', 'YearsInCurrentRole',
                           'YearsSinceLastPromotion', 'YearsWithCurrManager',
                           'BusinessTravel', 'Department', 'EducationField', 'Gender', 'JobRole',
                           'MaritalStatus', 'OverTime']

# --- HTML Template for the form ---
# We are embedding the HTML directly in the Python code for simplicity.
# For larger applications, this would typically be in a separate .html file.
HTML_FORM_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Employee Attrition Prediction</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f4f4f4; color: #333; }
        .container { background-color: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 800px; margin: auto; }
        h1, h2 { color: #0056b3; }
        form div { margin-bottom: 10px; }
        label { display: inline-block; width: 200px; font-weight: bold; }
        input[type="number"], input[type="text"] { width: calc(100% - 220px); padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #0056b3; }
        .note { font-size: 0.9em; color: #666; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
        .prediction-result { margin-top: 20px; padding: 15px; border: 1px solid #28a745; background-color: #e6ffe6; border-radius: 5px; }
        .error-message { margin-top: 20px; padding: 15px; border: 1px solid #dc3545; background-color: #ffe6e6; border-radius: 5px; color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Employee Attrition Predictor</h1>
        <p>Fill in the employee details below to get an attrition prediction.</p>

        <form method="POST" action="/predict_form">
            {% for feature in features %}
            <div>
                <label for="{{ feature }}">{{ feature }}:</label>
                <input type="number" id="{{ feature }}" name="{{ feature }}" value="{{ initial_values.get(feature, '') }}" required>
            </div>
            {% endfor %}
            <button type="submit">Get Prediction</button>
        </form>

        {% if prediction_result %}
        <div class="prediction-result">
            <h2>Prediction Result:</h2>
            <p><strong>Prediction:</strong> {{ prediction_result.prediction }}</p>
            <p><strong>Probability (No Attrition):</strong> {{ "%.2f" | format(prediction_result.probability_no_attrition) }}</p>
            <p><strong>Probability (Yes Attrition):</strong> {{ "%.2f" | format(prediction_result.probability_yes_attrition) }}</p>
        </div>
        {% endif %}

        {% if error_message %}
        <div class="error-message">
            <h2>Error:</h2>
            <p>{{ error_message }}</p>
        </div>
        {% endif %}

        <div class="note">
            <h3>Note on Categorical Features:</h3>
            <p>Please enter numerical values for the following features as they were converted during model training:</p>
            <ul>
                <li><strong>BusinessTravel:</strong> 0 (No Travel), 1 (Travel_Frequently), 2 (Travel_Rarely)</li>
                <li><strong>Department:</strong> 0 (Human Resources), 1 (Research & Development), 2 (Sales)</li>
                <li><strong>EducationField:</strong> (depends on your specific encoding, e.g., 0 for HR, 1 for Life Sciences, etc.) - Refer to your `model_dev.py`'s LabelEncoder output if unsure.</li>
                <li><strong>Gender:</strong> 0 (Female), 1 (Male)</li>
                <li><strong>JobRole:</strong> (numerical value based on your specific encoding, e.g., 0-8)</li>
                <li><strong>MaritalStatus:</strong> 0 (Divorced), 1 (Married), 2 (Single)</li>
                <li><strong>OverTime:</strong> 0 (No), 1 (Yes)</li>
            </ul>
            <p>The example values in the form are for demonstration. Use values that make sense for your data.</p>
        </div>
    </div>
</body>
</html>
"""

# --- Define API Endpoints ---
@app.route('/')
def home():
    return "<h1>Welcome to the Employee Attrition Predictor API!</h1><p>Send a POST request to /predict for JSON API or visit /predict_form for web interface.</p>"

# JSON API endpoint (existing)
@app.route('/predict', methods=['POST'])
def predict_json():
    if model is None or scaler is None:
        return jsonify({'error': 'Model or scaler not loaded on server.'}), 500

    try:
        data = request.json

        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid input format. Expected a JSON object (dictionary).'}), 400

        # Convert the incoming JSON data to a pandas DataFrame, ensuring column order
        input_df = pd.DataFrame([data], columns=expected_features_order)
        input_array = input_df.values

        # Scale the input data using the loaded scaler
        data_scaled = scaler.transform(input_array)

        # Make Prediction
        prediction = model.predict(data_scaled)
        prediction_proba = model.predict_proba(data_scaled)

        churn_status = "Yes Attrition" if prediction[0] == 1 else "No Attrition"

        response = {
            'prediction': churn_status,
            'raw_prediction': int(prediction[0]),
            'probability_no_attrition': float(prediction_proba[0][0]),
            'probability_yes_attrition': float(prediction_proba[0][1])
        }
        return jsonify(response)

    except KeyError as ke:
        return jsonify({'error': f"Missing input feature: {ke}. Please provide all expected features."}), 400
    except Exception as e:
        return jsonify({'error': f"An error occurred during prediction: {str(e)}", "message": "Ensure your input data matches the model's expectations (data types, completeness, feature order, and proper encoding for categorical values if applicable)."}), 500

# New web form endpoint for user-friendly input
@app.route('/predict_form', methods=['GET', 'POST'])
def predict_form():
    prediction_result = None
    error_message = None
    initial_values = {}

    if request.method == 'POST':
        if model is None or scaler is None:
            error_message = 'Model or scaler not loaded on server. Please check server logs.'
            return render_template_string(HTML_FORM_TEMPLATE, features=expected_features_order, prediction_result=prediction_result, error_message=error_message, initial_values=initial_values)

        try:
            # Get data from form
            form_data = request.form.to_dict()
            initial_values = form_data # To repopulate the form

            # Convert form data to correct types (all from form are strings)
            # Make sure numerical features are int/float
            # Categorical features are expected as numerical input from the form
            processed_data = {}
            for feature in expected_features_order:
                val = form_data.get(feature)
                if val is None:
                    raise KeyError(feature) # Ensure all features are provided

                # Attempt to convert to number, assuming all features are numerical after encoding
                try:
                    processed_data[feature] = float(val) if '.' in val else int(val)
                except ValueError:
                    error_message = f"Invalid value for {feature}. Please enter a numerical value."
                    return render_template_string(HTML_FORM_TEMPLATE, features=expected_features_order, prediction_result=prediction_result, error_message=error_message, initial_values=initial_values)


            input_df = pd.DataFrame([processed_data], columns=expected_features_order)
            input_array = input_df.values

            # Scale the input data
            data_scaled = scaler.transform(input_array)

            # Make Prediction
            prediction = model.predict(data_scaled)
            prediction_proba = model.predict_proba(data_scaled)

            churn_status = "Yes Attrition" if prediction[0] == 1 else "No Attrition"

            prediction_result = {
                'prediction': churn_status,
                'raw_prediction': int(prediction[0]),
                'probability_no_attrition': float(prediction_proba[0][0]),
                'probability_yes_attrition': float(prediction_proba[0][1])
            }

        except KeyError as ke:
            error_message = f"Missing input for feature: {ke}. Please fill in all fields."
        except Exception as e:
            error_message = f"An error occurred during prediction: {str(e)}. Ensure all fields have valid numerical values."
    
    # Pre-fill some default/example values for a more user-friendly initial form load
    # You might want to get these from your employee_data.csv for realistic examples
    if not initial_values: # Only set defaults if no form has been submitted yet
        initial_values = {
            "Age": 35, "DailyRate": 1200, "DistanceFromHome": 10, "Education": 3,
            "EnvironmentSatisfaction": 3, "HourlyRate": 80, "JobInvolvement": 3,
            "JobLevel": 2, "JobSatisfaction": 3, "MonthlyIncome": 6500,
            "MonthlyRate": 15000, "NumCompaniesWorked": 3, "PercentSalaryHike": 12,
            "PerformanceRating": 3, "RelationshipSatisfaction": 3, "StockOptionLevel": 1,
            "TotalWorkingYears": 7, "TrainingTimesLastYear": 2, "WorkLifeBalance": 3,
            "YearsAtCompany": 5, "YearsInCurrentRole": 3, "YearsSinceLastPromotion": 1,
            "YearsWithCurrManager": 4, "BusinessTravel": 2, "Department": 2,
            "EducationField": 1, "Gender": 0, "JobRole": 7, "MaritalStatus": 2, "OverTime": 1
        }


    return render_template_string(HTML_FORM_TEMPLATE, features=expected_features_order, prediction_result=prediction_result, error_message=error_message, initial_values=initial_values)


if __name__ == '__main__':
    print("\n--- Starting Flask API server ---")
    print("API is running locally. You can access it at:")
    print("  Home page: http://127.0.0.1:5000/")
    print("  Web Form for Prediction: http://127.0.0.1:5000/predict_form (Use your browser)")
    app.run(debug=True, host='0.0.0.0', port=5000)