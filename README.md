# Task-3--End-to-End DataScience Project

*Company*   : CODTECH IT SOLUTIONS

*Name*      : Rachabattuni Sai Sindhu

*Intern ID* : CT06DG1263

*Domain*    : Data Science

*Duration*  : 6 Weeks

*Mentor*    : Neela Santosh

###
hello there, Task 3 focused on building a complete end-to-end data science project, starting from a raw dataset and ending with a fully deployed machine learning model accessible through a web-based API. The primary goal was to develop a predictive system for employee attrition identifying whether an employee is likely to leave the organization based on various features such as job role, experience, satisfaction, and work environment.
This task was designed to simulate a real-world industry workflow. It involved key stages such as data cleaning, preprocessing, model development, deployment, API integration, and testing all using Python. What made this task particularly impactful was that it required not just training a machine learning model but also wrapping it into a usable tool that can take live input and return predictions in real-time.
For someone like me, who is still new to the field of data science and Python programming, this task provided a clear pathway to understanding how data science solutions are built, tested, and shared for practical use. The emphasis was not only on writing correct code, but also on building something that others can use and understand a valuable skill in any real-world data role.
The real-world value of this project lies in helping organizations anticipate employee resignations so they can proactively implement retention strategies. As a beginner in Python and data science tools, this task allowed me to explore the full journey from handling raw data to creating a live, interactive prediction system.

### 1. Dataset and Problem Understanding
The dataset I worked with, employee_data.csv, was sourced from Kaggle. It contained detailed records of employees such as department, job role, education, work experience, satisfaction levels, and their attrition status (Yes or No). The main goal was to analyze this historical data and train a machine learning model that could predict whether a new employee was at risk of leaving.

### 2. Environment Setup
As someone new to Python and its tools, setting up the environment was my first challenge. I created a virtual environment called datascience_env using Python's built-in venv module. Inside this environment, I installed key libraries including:
* pandas for data analysis
* numpy for numerical operations
* scikit-learn for machine learning
* flask for web development
* requests for testing the API
This helped keep my project clean and isolated from other Python installations.

### 3. Model Development and Preprocessing
I created a script named model_dev.py that took care of the entire model training process. The major steps were:
* **Loading Data:** Read the CSV file into a Pandas DataFrame.
* **Cleaning:** Removed unnecessary columns like EmployeeCount, Over18, etc.
* **Encoding:** Converted text-based categorical features into numerical form using LabelEncoder.
* **Scaling:** Used StandardScaler to normalize numerical features for better model performance.
* **Training:** Used a RandomForestClassifier to train the model on a split training dataset.
* **Saving the Model:** Used pickle to save the trained model and the scaler for future use.
Despite being a beginner, these steps gave me hands-on experience with real preprocessing and model development.

### 5. API Development Using Flask
With the trained model ready, I built a simple but powerful Flask application (app.py) to deploy it. It had two routes:
* /predict: Accepts POST requests with employee data in JSON format and returns whether the employee is likely to leave.
* /predict_form: Renders an HTML form where a user can enter employee data and view the prediction in their browser.
The Flask app loaded the saved model and scaler, processed the input, made predictions, and returned results in real time.

### 6. API Testing and Debugging
To test the API, I created another script called test_api.py. It used the requests library to send POST requests to the Flask server. Initially, I faced errors like:
* Flask app not running (Connection refused)
* Missing libraries (ModuleNotFoundError)
* Input mismatches
I resolved them step by step learning how to run the Flask app in one terminal and test it from another. Adding pretty-printing using json.dumps() helped make the JSON responses easier to read.

### 7. Adding a Web Interface for Ease of Use
As a beginner, I realized that writing JSON each time for testing wasn’t practical for many users. So, I added a simple HTML form inside the Flask app via the /predict_form route. This allowed users to enter data manually and get predictions through a friendly browser interface. It was a rewarding experience to see the project evolve into something interactive.

### 8.What i have learned
As a beginner in Python, machine learning, and Flask, this task gave me a hands-on understanding of how complete data science projects are built and deployed.
Data Preprocessing: I learned how to clean and prepare data, encode categorical features, and scale numerical values to make them suitable for machine learning models.
Model Training: I gained experience using a RandomForestClassifier, splitting data for training and testing, evaluating model accuracy, and saving the model and scaler using pickle.
Flask API Development: I built a simple API that loads the model and makes predictions through both a JSON endpoint and an HTML form. This taught me how to create interactive and usable web-based ML applications.
Testing and Debugging: I faced and fixed beginner-level issues like environment setup, API connectivity, and missing modules, which improved my troubleshooting skills.
Overall, I learned how to connect every part of a project—from raw data to a fully working, user-friendly prediction system.

### 9. Conclusion
As of completing Task 3 was a huge milestone in my learning journey. As a beginner, I didn’t just train a model I built a fully functional prediction system, deployed it with an API, created a user-friendly web interface, and documented everything professionally.
This task helped me connect the dots between theory and practical application. It showed me how to think like a data scientist not only in terms of code, but also in terms of building solutions that others can use. Now, I feel much more confident in my ability to take on real-world data problems and build complete projects from start to finish.
This experience has strengthened both my technical and problem-solving skills, and I’m excited to keep learning and building even more advanced projects in the future.


### Output:

Module evaluation is done at first..
![Image](https://github.com/user-attachments/assets/7bf55200-3f37-40cb-8432-ed9567ee97e7)

and then application to be runned...
for that a API is created..
![Image](https://github.com/user-attachments/assets/f4c41197-acbd-4da2-80b3-516326064637)

![Image](https://github.com/user-attachments/assets/2f12e585-af50-4e1d-a57f-1524fbb145c7)

and then a web form for
![Image](https://github.com/user-attachments/assets/f0bbd573-be7f-4bd3-be10-0542b8ad829a)
![Image](https://github.com/user-attachments/assets/1a09f126-1604-41fc-8e49-9fc44fcbb095)

and testing and debugginf of model is done
![Image](https://github.com/user-attachments/assets/2d361ad4-28e1-49d2-bd33-01f43eb4689e)
![Image](https://github.com/user-attachments/assets/4706fd0f-8886-42d3-8302-4fa4e14015f9)
