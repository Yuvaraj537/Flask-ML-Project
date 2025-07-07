from flask import Flask, request, render_template
from datetime import datetime

app = Flask(__name__)

def get_int(field):
    val = request.form.get(field)
    if val is None or val.strip() == '':
        raise ValueError(f"Missing or empty field: {field}")
    return int(val)

def get_float(field):
    val = request.form.get(field)
    if val is None or val.strip() == '':
        raise ValueError(f"Missing or empty field: {field}")
    return float(val)

def calculate_emi(principal, annual_interest_rate, tenure_months):
    """
    Calculate monthly EMI using formula:
    EMI = [P x r x (1+r)^n] / [(1+r)^n-1]
    where
    P = principal loan amount
    r = monthly interest rate = annual_interest_rate / (12 * 100)
    n = tenure in months
    """
    r = annual_interest_rate / (12 * 100)
    n = tenure_months
    if r == 0:
        emi = principal / n
    else:
        emi = (principal * r * (1 + r)**n) / ((1 + r)**n - 1)
    return emi

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        loan_amount = get_float('loan_amount')
        loan_months = get_int('loan_months')
        interest_rate = get_float('interest_rate')

        if loan_amount <= 0 or loan_months <= 0:
            return render_template('index.html', error="Loan amount and tenure must be positive.")
        if interest_rate < 0:
            return render_template('index.html', error="Interest rate cannot be negative.")

        emi = calculate_emi(loan_amount, interest_rate, loan_months)
        total_payable = emi * loan_months
        total_interest = total_payable - loan_amount

        def fmt_amt(amount):
            return f"₹{amount:,.2f}"

        emi_fmt = fmt_amt(emi)
        total_interest_fmt = fmt_amt(total_interest)
        total_payable_fmt = fmt_amt(total_payable)
        loan_amount_fmt = fmt_amt(loan_amount)

        #prediction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prediction_date = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        result_string = (
            "Prediction \n"
            f"Monthly EMI: {emi_fmt}\n"
            f"Total Interest : {total_interest_fmt}\n"
            f"Total Payable : {total_payable_fmt}\n"
            f"Original Loan Amount: {loan_amount_fmt}\n"
            f"Loan Tenure (Months): {loan_months}\n"
            f"Calculation made on: {prediction_date}"
        )

        return render_template('index.html', result=result_string, error=None)

    except Exception as e:
        return render_template('index.html', error=f"Error occurred: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
