from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model safely
model = pickle.load(open("lung cancer_model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        gender = int(request.form['gender'])
        age = int(request.form['age'])
        cancer_stage = int(request.form['cancer_stage'])
        family_history = int(request.form['family_history'])
        smoking_status = int(request.form['smoking_status'])
        bmi = float(request.form['bmi'])
        cholesterol_level = int(request.form['cholesterol_level'])
        hypertension = int(request.form['hypertension'])
        asthma = int(request.form['asthma'])
        cirrhosis = int(request.form['cirrhosis'])
        treatment_type = int(request.form['treatment_type']) 

        input_data = np.array([[
            gender, age, cancer_stage, family_history,
            smoking_status, bmi, cholesterol_level,
            hypertension, asthma, cirrhosis,
            treatment_type
        ]])

        prediction = model.predict(input_data)[0]
        result = "survived" if prediction == 1 else "Not survived"

        return render_template("index.html", prediction_text=f"Survival Risk: {result}")
    
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error occurred: {str(e)}")


if __name__ == '__main__':
    app.run(debug=True)