# model_dev.py
# This script performs data preprocessing, trains an employee attrition prediction model,
# evaluates it, and saves the trained model and scaler for later use in the API.

import pandas as pd # Library for data manipulation and analysis
from sklearn.model_selection import train_test_split # To split data into training and testing sets
from sklearn.preprocessing import LabelEncoder, StandardScaler # For data encoding and scaling
from sklearn.ensemble import RandomForestClassifier # The machine learning model we will use
from sklearn.metrics import accuracy_score # To evaluate model performance
import pickle # Built-in Python module for serializing (saving) and deserializing (loading) objects

print("--- Starting Data Preprocessing and Model Training Pipeline ---")

# --- 1. Load Dataset ---
# This line reads your CSV file into a pandas DataFrame.
# It expects the file 'employee_data.csv' to be in the same directory as this script.
print("\nLoading employee_data.csv...")
try:
    df = pd.read_csv('employee_data.csv')
    print("Dataset loaded successfully. First 5 rows:")
    print(df.head()) # Display the first few rows to confirm loading
    print(f"\nDataset shape: {df.shape} (Rows, Columns)")
except FileNotFoundError:
    # This error occurs if the CSV file isn't found at the specified path.
    print("Error: 'employee_data.csv' not found in the current directory.")
    print("Please ensure the CSV file is renamed to 'employee_data.csv' and placed directly in the 'employee_attrition' folder.")
    # Exiting the script because we can't proceed without data
    exit()

# --- 2. Drop irrelevant columns ---
# These columns are typically unique identifiers (EmployeeNumber) or constant values
# across the dataset (EmployeeCount, Over18, StandardHours) and don't help in prediction.
print("\nDropping irrelevant columns (EmployeeCount, Over18, StandardHours, EmployeeNumber)...")
df.drop(['EmployeeCount', 'Over18', 'StandardHours', 'EmployeeNumber'], axis=1, inplace=True)
print(f"New dataset shape after dropping columns: {df.shape}")

# --- 3. Convert categorical columns using LabelEncoder ---
# Machine learning models work with numbers, not text.
# LabelEncoder converts unique text categories into unique numbers (e.g., 'Yes' -> 1, 'No' -> 0).
# This process is applied to all columns that have 'object' (string) data type.
le = LabelEncoder() # Create an instance of the LabelEncoder
print("\nEncoding categorical columns to numerical values:")
for column in df.select_dtypes(include=['object']).columns:
    print(f"  Encoding column: '{column}'")
    df[column] = le.fit_transform(df[column]) # Apply encoding to the column

print("\nCategorical columns encoded. First 5 rows of the modified DataFrame:")
print(df.head()) # Observe how text columns are now numbers

# --- 4. Split features and target ---
# We separate the data into features (X), which are the input columns used for prediction,
# and the target (y), which is the column we want to predict ('Attrition').
# 'Attrition' was already converted to 1 (Yes) or 0 (No) by LabelEncoder.
X = df.drop('Attrition', axis=1) # X contains all columns EXCEPT 'Attrition'
y = df['Attrition']  # y contains only the 'Attrition' column

print(f"\nFeatures (X) shape: {X.shape}")
print(f"Target (y) shape: {y.shape}")

# --- 5. Scale the numerical data ---
# Scaling is crucial for many ML algorithms. StandardScaler transforms numerical features
# so they have a mean of 0 and a standard deviation of 1. This prevents features with
# larger values from disproportionately influencing the model.
scaler = StandardScaler() # Create an instance of the StandardScaler
print("\nScaling numerical features using StandardScaler...")
X_scaled = scaler.fit_transform(X) # Fit the scaler to X and then transform X

print("Features scaled. First 5 rows of the scaled feature array (X_scaled):")
# Note: X_scaled is a NumPy array, not a DataFrame, after scaling.
print(X_scaled[:5])

# --- 6. Train-test split ---
# We split the scaled data into two sets:
#   - Training set (80%): Used to train the model.
#   - Testing set (20%): Used to evaluate how well the trained model performs on unseen data.
# random_state=42 ensures that your split is the same every time you run the script.
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

print(f"\nData split into training ({len(X_train)} samples) and testing ({len(X_test)} samples).")
print(f"X_train shape: {X_train.shape}, y_train shape: {y_train.shape}")
print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")


# --- 7. Train model ---
# RandomForestClassifier is a powerful and popular machine learning model
# for classification tasks. It builds multiple decision trees and combines their outputs.
print("\nTraining RandomForestClassifier model...")
model = RandomForestClassifier(random_state=42) # Initialize the model
model.fit(X_train, y_train) # Train the model on the training data
print("Model training complete.")

# --- 8. Evaluate ---
# We use the trained model to make predictions on the unseen test set
# and then compare these predictions to the actual values (y_test)
# to calculate the accuracy.
y_pred = model.predict(X_test) # Make predictions on the test set
accuracy = accuracy_score(y_test, y_pred) # Calculate the accuracy
print(f"\nModel Evaluation on Test Set:")
print(f"Accuracy: {accuracy:.4f}") # Print accuracy (formatted to 4 decimal places)

# --- 9. Save model and scaler ---
# It's crucial to save both the trained model and the scaler.
# When new data comes into your API for prediction, it must be preprocessed
# using the *exact same* scaling and encoding rules that were used during training.
# 'wb' mode means "write binary" mode.
print("\nSaving trained model (model.pkl) and scaler (scaler.pkl)...")
try:
    pickle.dump(model, open("model.pkl", "wb")) # Save the trained model
    pickle.dump(scaler, open("scaler.pkl", "wb")) # Save the fitted scaler
    print("Model and Scaler saved successfully! You should now see 'model.pkl' and 'scaler.pkl' in your folder.")
except Exception as e:
    print(f"Error saving model or scaler: {e}")

print("\n--- Model Development Pipeline Finished ---")