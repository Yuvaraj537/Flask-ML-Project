from flask import Flask, request, render_template
import pickle
import numpy as np  # Needed for model prediction

app = Flask(__name__)

# Load trained model
model = pickle.load(open('pizza.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect form data
        Restaurant_Name = int(request.form.get('Restaurant Name'))
        Location_Name = int(request.form.get('Location'))
        Delivery_Duration = int(request.form.get('Delivery Duration (min)'))
        Pizza_Size = int(request.form.get('Pizza Size'))
        Pizza_Type = int(request.form.get('Pizza Type'))
        Toppings_Count = int(request.form.get('Toppings Count'))
        Distance = float(request.form.get('Distance (Km)'))
        Traffic_Level = int(request.form.get('Traffic_Level'))
        Payment_Method = int(request.form.get('Payment Method'))
        Topping_Density = float(request.form.get('Topping Density'))
        Payment_Category = int(request.form.get('Payment_Category'))

        # Combine into input format
        input_data = [[
            Restaurant_Name,
            Location_Name,
            Delivery_Duration,
            Pizza_Size,
            Pizza_Type,
            Toppings_Count,
            Distance,
            Traffic_Level,
            Payment_Method,
            Topping_Density,
            Payment_Category
        ]]

        # Rule-based prediction based on distance
        if 0 <= Distance <= 5:
            result = "Not Delayed"
            reason = "Good Delivery"
        elif 5 < Distance <= 7:
            result = "Delayed"
            reason = " Not Good delivery"
        else:
            # Use ML model for longer distances
            prediction = model.predict(np.array(input_data))
            if prediction[0] == 0:
                result = "Not Delayed"
                reason = "Predicted by ML model as on-time delivery."
            else:
                result = "Delayed"
                reason = "delayed based  on travel"

        # Show prediction
        output = f"Prediction: {result} | Reason: {reason}"
        return render_template('index.html', prediction_text=output)

    except Exception as e:
        return f"Error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)

