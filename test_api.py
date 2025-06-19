# test_api.py
import requests
import json # Added import for json module

# --- IMPORTANT: FILL IN REALISTIC NUMERICAL VALUES FOR EACH FEATURE ---
# These values must correspond to the order of expected_features_order in app.py.
# For categorical features, use the numerical values that LabelEncoder assigned in model_dev.py.
test_data = {
    "Age": 30,
    "DailyRate": 800,
    "DistanceFromHome": 5,
    "Education": 3,
    "EnvironmentSatisfaction": 3,
    "HourlyRate": 70,
    "JobInvolvement": 3,
    "JobLevel": 1,
    "JobSatisfaction": 4,
    "MonthlyIncome": 4000,
    "MonthlyRate": 10000,
    "NumCompaniesWorked": 2,
    "PercentSalaryHike": 15,
    "PerformanceRating": 3,
    "RelationshipSatisfaction": 3,
    "StockOptionLevel": 1,
    "TotalWorkingYears": 5,
    "TrainingTimesLastYear": 2,
    "WorkLifeBalance": 3,
    "YearsAtCompany": 3,
    "YearsInCurrentRole": 2,
    "YearsSinceLastPromotion": 1,
    "YearsWithCurrManager": 2,
    "BusinessTravel": 2, # Example: 0=No Travel, 1=Travel_Frequently, 2=Travel_Rarely
    "Department": 1,     # Example: 0=HR, 1=R&D, 2=Sales
    "EducationField": 3, # Example: 0=HR, 1=Life Sciences, 2=Marketing, 3=Medical, 4=Other, 5=Technical Degree
    "Gender": 1,         # Example: 0=Female, 1=Male
    "JobRole": 5,        # Example: 0=Healthcare Rep, ..., 5=Laboratory Technician, ...
    "MaritalStatus": 1,  # Example: 0=Divorced, 1=Married, 2=Single
    "OverTime": 0        # Example: 0=No, 1=Yes
}

url = 'http://127.0.0.1:5000/predict'
headers = {'Content-Type': 'application/json'}

# Send the POST request
response = requests.post(url, data=json.dumps(test_data), headers=headers)

# Print the JSON response from the API, pretty-printed
print(json.dumps(response.json(), indent=4))