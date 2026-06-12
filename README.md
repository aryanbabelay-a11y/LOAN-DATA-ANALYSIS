# LOAN-DATA-ANALYSIS
1. Project Overview
This project analyzes 1,00,000 loan applicant records to identify demographic, financial, and behavioral risk factors associated with loan defaults in India. The pipeline covers end-to-end data analysis: ingestion, EDA, SQL querying, and Power BI dashboard design.

## 2. Dataset Information
File
Applicant-details.csv

Shape
Rows: 1,00,000   |   Columns: 13

Target Variable
Loan_Default_Risk   |   0 = Safe Applicant   |   1 = Defaulter

Data Dictionary

Column Name	Data Type	Values / Range	Description
Applicant_ID	INT	Unique	Applicant identifier
Annual_Income	INT	10K - 1Cr INR	Gross yearly income
Applicant_Age	INT	18 - 90	Age of applicant
Work_Experience	INT	0 - 20 years	Total work experience
Marital_Status	VARCHAR	single / married	Marital status
House_Ownership	VARCHAR	rented/owned/norent_noown	Housing situation
Vehicle_Ownership(car)	VARCHAR	yes / no	Car ownership flag
Occupation	VARCHAR	51 categories	Job type
Residence_City	VARCHAR	317 cities	City of residence
Residence_State	VARCHAR	29 states	State of residence
Years_in_Current_Employment	INT	0 - 20	Job stability
Years_in_Current_Residence	INT	10 - 14	Residence stability
Loan_Default_Risk	INT	0 or 1	Target: default risk

## 3. Project Structure
loan-analysis/
   Applicant-details.csv       <- Raw dataset
   loan_eda.py                 <- Python EDA script
   loan_sql_queries.sql        <- All PostgreSQL queries
   Loan_Analysis_Report.docx   <- Full analysis report
   README.docx                 <- This file
   powerbi/
      Loan_Dashboard.pbix      <- Power BI dashboard

## 4. Setup & Installation
Python Dependencies
pip install pandas numpy matplotlib seaborn sqlalchemy psycopg2-binary

Database Setup (PostgreSQL)
CREATE DATABASE loan_db;
\c loan_db
-- Then run the CREATE TABLE from loan_sql_queries.sql

Load CSV into PostgreSQL
COPY applicants FROM '/path/to/Applicant-details.csv'
  DELIMITER ',' CSV HEADER;

Run Python EDA
python loan_eda.py

## 5. SQL Queries Covered

Query #	Question
Q1	Overall default rate
Q2	Default rate by house ownership
Q3	Default rate by marital status
Q4	Default rate by vehicle ownership
Q5	Default rate by income bracket (CASE in GROUP BY)
Q6	Default rate by age group (CASE in GROUP BY)
Q7	Top 10 riskiest occupations (HAVING COUNT >= 100)
Q8	Top 10 riskiest states
Q9	Avg income / age / experience: defaulters vs non-defaulters
Q10	Combined risk: house + marital + vehicle

Note: All ROUND() calls use ::NUMERIC cast to avoid PostgreSQL double-precision errors.

## 6. Power BI Dashboard
DAX Measures Required
Total Applicants  = COUNTROWS(applicants)
Total Defaulters  = CALCULATE(COUNTROWS(applicants), applicants[Loan_Default_Risk]=1)
Default Rate %    = DIVIDE([Total Defaulters],[Total Applicants])*100
Avg Income        = AVERAGE(applicants[Annual_Income])

Recommended Visuals

Visual Type	Columns Used	Insight
KPI Cards	Total, Defaulters, Default Rate%	Executive summary
Donut Chart	Loan_Default_Risk	Safe vs Defaulter split
Bar Chart	House_Ownership + Default Rate	Housing risk
Bar Chart	Age_Group + Default Rate	Age risk bands
Bar Chart	Occupation + Default Rate (Top 15)	Risky professions
Map Visual	Residence_State + Default Rate	Geographic risk
Donut Chart	Vehicle_Ownership	Asset proxy
Scatter Plot	Income vs Work_Experience	Risk clustering
Slicers	State, House_Ownership, Income_Bracket	Interactivity

## 7. Key Findings Summary
•Overall default rate: 13.0% (12,997 out of 1,00,000)
•Renters default 48% more than homeowners (13.34% vs 9.01%)
•Non-car-owners default 44% more than car owners (14.33% vs 9.94%)
•Single applicants default more than married (13.22% vs 11.02%)
•Youngest group (<25 yrs) has the highest default rate at 14.57%
•Income bracket alone is NOT a reliable predictor — rates are flat across all brackets
•Manipur has the highest state-level default rate at 25.74%
•Police Officer is the riskiest occupation at 18.61% default rate

## 8. Notes & Limitations
•Dataset appears synthetic — real-world income-default relationships would be stronger
•Years_in_Current_Residence has very low variance (range 10-14), limiting its predictive value
•No temporal data available — cannot track default over loan tenure
•Consider SMOTE or class weighting for any future ML modeling due to 87:13 class imbalance
