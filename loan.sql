-- Create table
CREATE TABLE applicants (
    applicant_id                 INT,
    annual_income                BIGINT,
    applicant_age                INT,
    work_experience              INT,
    marital_status               VARCHAR(20),
    house_ownership              VARCHAR(20),
    vehicle_ownership            VARCHAR(5),
    occupation                   VARCHAR(100),
    residence_city               VARCHAR(100),
    residence_state              VARCHAR(100),
    years_in_current_employment  INT,
    years_in_current_residence   INT,
    loan_default_risk            INT
);
SELECT * FROM applicants
-- Q1: Overall default rate
SELECT
    COUNT(*) AS total_applicants,
    SUM(loan_default_risk) AS total_defaulters,
    ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants;

-- Q2: Default rate by house ownership
SELECT house_ownership,
       COUNT(*) AS total,
       SUM(loan_default_risk) AS defaulters,
       ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY house_ownership
ORDER BY default_rate_pct DESC;

-- Q3: Default rate by marital status
SELECT marital_status,
       COUNT(*) AS total,
       ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY marital_status;

-- Q4: Default rate by vehicle ownership
SELECT vehicle_ownership,
       COUNT(*) AS total,
       ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY vehicle_ownership;

-- Q5: Default rate by income bracket
SELECT
    CASE
        WHEN annual_income < 2500000  THEN 'Low'
        WHEN annual_income < 5000000  THEN 'Medium'
        WHEN annual_income < 7500000  THEN 'High'
        ELSE 'Very High'
    END AS income_bracket,
    COUNT(*) AS total,
    ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY
    CASE
        WHEN annual_income < 2500000  THEN 'Low'
        WHEN annual_income < 5000000  THEN 'Medium'
        WHEN annual_income < 7500000  THEN 'High'
        ELSE 'Very High'
    END
ORDER BY default_rate_pct DESC;

-- Q6: Default rate by age group
SELECT
    CASE
        WHEN applicant_age < 25 THEN '<25'
        WHEN applicant_age < 35 THEN '25-35'
        WHEN applicant_age < 45 THEN '35-45'
        WHEN applicant_age < 55 THEN '45-55'
        ELSE '55+'
    END AS age_group,
    COUNT(*) AS total,
    ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY
    CASE
        WHEN applicant_age < 25 THEN '<25'
        WHEN applicant_age < 35 THEN '25-35'
        WHEN applicant_age < 45 THEN '35-45'
        WHEN applicant_age < 55 THEN '45-55'
        ELSE '55+'
    END
ORDER BY default_rate_pct DESC;

-- Q7: Top 10 occupations by default rate (min 100 applicants)
SELECT occupation,
       COUNT(*) AS total,
       ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY occupation
HAVING COUNT(*) >= 100
ORDER BY default_rate_pct DESC
LIMIT 10;

-- Q8: Top 10 states by default rate
SELECT residence_state,
       COUNT(*) AS total,
       SUM(loan_default_risk) AS defaulters,
       ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY residence_state
ORDER BY default_rate_pct DESC
LIMIT 10;

-- Q9: Avg income of defaulters vs non-defaulters
SELECT
    CASE WHEN loan_default_risk = 1 THEN 'Defaulter' ELSE 'Non-Defaulter' END AS risk_label,
    ROUND(AVG(annual_income)) AS avg_income,
    ROUND(AVG(applicant_age), 1) AS avg_age,
    ROUND(AVG(work_experience), 1) AS avg_experience
FROM applicants
GROUP BY loan_default_risk;

-- Q10: Combined risk factors
SELECT house_ownership, marital_status, vehicle_ownership,
       COUNT(*) AS total,
       ROUND(AVG(loan_default_risk::NUMERIC) * 100, 2) AS default_rate_pct
FROM applicants
GROUP BY house_ownership, marital_status, vehicle_ownership
ORDER BY default_rate_pct DESC;