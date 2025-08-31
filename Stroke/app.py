from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model safely
model = pickle.load(open("stroke_model.pkl", "rb"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Convert all inputs to integers
        gender = int(request.form['gender'])
        age = int(request.form['age'])
        hypertension = int(request.form['hypertension'])
        heart_disease = int(request.form['heart_disease'])
        ever_married = int(request.form['ever_married'])
        work_type = int(request.form['work_type'])
        residence_type = int(request.form['residence_type'])
        avg_glucose_level = int(request.form['avg_glucose_level'])
        bmi = int(request.form['bmi'])
        smoking_status = int(request.form['smoking_status'])

        input_data = np.array([[gender, age, hypertension, heart_disease,
                                ever_married, work_type, residence_type,
                                avg_glucose_level, bmi, smoking_status]])

        # Make prediction
        prediction = model.predict(input_data)[0]
        result = "Stroke" if prediction == 1 else "No Stroke"

        #return render_template('index.html', prediction_text=f"Prediction: {result}")
        return render_template("index.html", prediction_text=f"Stroke Risk: {result}")


    except Exception as e:
        return render_template('index.html', prediction_text=f"Error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
