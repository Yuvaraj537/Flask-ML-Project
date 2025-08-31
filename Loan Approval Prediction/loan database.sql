create database loan_db;
use loan_db;
CREATE TABLE emi_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    loan_amount FLOAT,
    loan_months INT,
    interest_rate FLOAT,
    emi FLOAT,
    total_interest FLOAT,
    total_payable FLOAT,
    prediction_date DATETIME
);
select * from emi_predictions;
drop table emi_predictions;