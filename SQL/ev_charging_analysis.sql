-- ============================================================
-- PROJECT: EV CHARGING STATION ANALYTICS
-- DATABASE: ev_charging
-- TABLE: charging_sessions
-- SQL DIALECT: MySQL 8.0+
-- ============================================================

USE ev_charging;


-- ============================================================
-- QUERY 1: TOTAL NUMBER OF CHARGING SESSIONS
-- Business Question: How many charging sessions are recorded?
-- ============================================================

SELECT
    COUNT(*) AS total_sessions
FROM charging_sessions;


-- ============================================================
-- QUERY 2: TOTAL REVENUE
-- Business Question: How much revenue was generated?
-- ============================================================

SELECT
    ROUND(SUM(Charging_Cost), 2) AS total_revenue
FROM charging_sessions;


-- ============================================================
-- QUERY 3: AVERAGE CHARGING COST
-- Business Question: What is the average cost per session?
-- ============================================================

SELECT
    ROUND(AVG(Charging_Cost), 2) AS average_charging_cost
FROM charging_sessions;


-- ============================================================
-- QUERY 4: REVENUE BY CITY
-- Business Question: Which city generates the highest revenue?
-- ============================================================

SELECT
    City,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue
FROM charging_sessions
GROUP BY City
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 5: CHARGING SESSIONS BY CITY
-- Business Question: Which city has the most charging sessions?
-- ============================================================

SELECT
    City,
    COUNT(*) AS total_sessions
FROM charging_sessions
GROUP BY City
ORDER BY total_sessions DESC;


-- ============================================================
-- QUERY 6: TOP 10 CUSTOMERS BY TOTAL SPENDING
-- Business Question: Who are the highest-spending customers?
-- ============================================================

SELECT
    Customer_ID,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Charging_Cost), 2) AS total_spent
FROM charging_sessions
GROUP BY Customer_ID
ORDER BY SUM(Charging_Cost) DESC
LIMIT 10;

-- ============================================================
-- QUERY 7: PERFORMANCE BY VEHICLE MANUFACTURER
-- Business Question: Which manufacturer generates the most revenue?
-- ============================================================

SELECT
    Manufacturer,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Energy_Consumed_kWh), 2) AS total_energy_consumed,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    ROUND(AVG(Charging_Cost), 2) AS average_session_cost
FROM charging_sessions
GROUP BY Manufacturer
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 8: PERFORMANCE BY CHARGER TYPE
-- Business Question: Which charger type generates more revenue?
-- ============================================================

SELECT
    Charger_Type,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Energy_Consumed_kWh), 2) AS total_energy_consumed,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    ROUND(AVG(Session_Duration_Minutes), 2) AS average_duration_minutes
FROM charging_sessions
GROUP BY Charger_Type
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 9: PAYMENT METHOD ANALYSIS
-- Business Question: Which payment method is used most frequently?
-- ============================================================

SELECT
    Payment_Method,
    COUNT(*) AS total_transactions,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    ROUND(AVG(Charging_Cost), 2) AS average_transaction_value
FROM charging_sessions
GROUP BY Payment_Method
ORDER BY total_transactions DESC;


-- ============================================================
-- QUERY 10: VEHICLE MODEL PERFORMANCE
-- Business Question: Which vehicle models consume the most energy?
-- ============================================================

SELECT
    Vehicle_Model,
    Manufacturer,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Energy_Consumed_kWh), 2) AS total_energy_consumed,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue
FROM charging_sessions
GROUP BY Vehicle_Model, Manufacturer
ORDER BY total_energy_consumed DESC;


-- ============================================================
-- QUERY 11: MONTHLY REVENUE
-- Business Question: How does revenue change over time?
-- ============================================================

SELECT
    YEAR(Start_Time) AS session_year,
    MONTH(Start_Time) AS session_month,
    DATE_FORMAT(Start_Time, '%Y-%m') AS month_year,
    ROUND(SUM(Charging_Cost), 2) AS monthly_revenue
FROM charging_sessions
GROUP BY
    YEAR(Start_Time),
    MONTH(Start_Time),
    DATE_FORMAT(Start_Time, '%Y-%m')
ORDER BY
    session_year,
    session_month;


-- ============================================================
-- QUERY 12: MONTHLY CHARGING SESSIONS
-- Business Question: How does charging activity change monthly?
-- ============================================================

SELECT
    YEAR(Start_Time) AS session_year,
    MONTH(Start_Time) AS session_month,
    DATE_FORMAT(Start_Time, '%Y-%m') AS month_year,
    COUNT(*) AS total_sessions
FROM charging_sessions
GROUP BY
    YEAR(Start_Time),
    MONTH(Start_Time),
    DATE_FORMAT(Start_Time, '%Y-%m')
ORDER BY
    session_year,
    session_month;


-- ============================================================
-- QUERY 13: RANK CITIES BY REVENUE
-- Business Question: What is each city's revenue ranking?
-- ============================================================

SELECT
    City,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(Charging_Cost) DESC
    ) AS revenue_rank
FROM charging_sessions
GROUP BY City
ORDER BY revenue_rank;


-- ============================================================
-- QUERY 14: RANK CUSTOMERS BY SPENDING
-- Business Question: Who are the highest-value customers?
-- ============================================================

SELECT
    Customer_ID,
    ROUND(SUM(Charging_Cost), 2) AS total_spent,
    COUNT(*) AS total_sessions,
    DENSE_RANK() OVER (
        ORDER BY SUM(Charging_Cost) DESC
    ) AS customer_rank
FROM charging_sessions
GROUP BY Customer_ID
ORDER BY customer_rank;


-- ============================================================
-- QUERY 15: TOP 3 VEHICLE MODELS BY REVENUE
-- WITHIN EACH MANUFACTURER
-- Business Question: Which models perform best for each manufacturer?
-- ============================================================

WITH vehicle_rank AS (
    SELECT
        Manufacturer,
        Vehicle_Model,
        COUNT(*) AS total_sessions,
        ROUND(SUM(Charging_Cost), 2) AS total_revenue,
        ROW_NUMBER() OVER (
            PARTITION BY Manufacturer
            ORDER BY SUM(Charging_Cost) DESC
        ) AS model_rank
    FROM charging_sessions
    GROUP BY Manufacturer, Vehicle_Model
)
SELECT
    Manufacturer,
    Vehicle_Model,
    total_sessions,
    total_revenue,
    model_rank
FROM vehicle_rank
WHERE model_rank <= 3
ORDER BY Manufacturer, model_rank;


-- ============================================================
-- QUERY 16: MONTH-OVER-MONTH REVENUE GROWTH
-- Business Question: Is revenue increasing or decreasing?
-- ============================================================

WITH monthly_revenue AS (
    SELECT
        CAST(
            DATE_FORMAT(Start_Time, '%Y-%m-01') AS DATE
        ) AS month_start,
        SUM(Charging_Cost) AS total_revenue
    FROM charging_sessions
    GROUP BY
        CAST(DATE_FORMAT(Start_Time, '%Y-%m-01') AS DATE)
),
revenue_comparison AS (
    SELECT
        month_start,
        total_revenue,
        LAG(total_revenue) OVER (
            ORDER BY month_start
        ) AS previous_month_revenue
    FROM monthly_revenue
)
SELECT
    DATE_FORMAT(month_start, '%Y-%m') AS month_year,
    ROUND(total_revenue, 2) AS current_month_revenue,
    ROUND(previous_month_revenue, 2) AS previous_month_revenue,
    ROUND(
        total_revenue - previous_month_revenue, 2
    ) AS revenue_change,
    ROUND(
        100.0 * (total_revenue - previous_month_revenue)
        / NULLIF(previous_month_revenue, 0),
        2
    ) AS growth_percentage
FROM revenue_comparison
ORDER BY month_start;


-- ============================================================
-- QUERY 17: RUNNING TOTAL OF MONTHLY REVENUE
-- Business Question: How does cumulative revenue grow over time?
-- ============================================================

WITH monthly_revenue AS (
    SELECT
        CAST(
            DATE_FORMAT(Start_Time, '%Y-%m-01') AS DATE
        ) AS month_start,
        SUM(Charging_Cost) AS monthly_revenue
    FROM charging_sessions
    GROUP BY
        CAST(DATE_FORMAT(Start_Time, '%Y-%m-01') AS DATE)
)
SELECT
    DATE_FORMAT(month_start, '%Y-%m') AS month_year,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(
        SUM(monthly_revenue) OVER (
            ORDER BY month_start
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS running_total_revenue
FROM monthly_revenue
ORDER BY month_start;


-- ============================================================
-- QUERY 18: CUSTOMER SEGMENTATION
-- Business Question: How can customers be grouped by spending?
-- Note: Thresholds are illustrative and can be adjusted.
-- ============================================================

WITH customer_spending AS (
    SELECT
        Customer_ID,
        COUNT(*) AS total_sessions,
        SUM(Charging_Cost) AS total_spent
    FROM charging_sessions
    GROUP BY Customer_ID
)
SELECT
    Customer_ID,
    total_sessions,
    ROUND(total_spent, 2) AS total_spent,
    CASE
        WHEN total_spent >= 10000 THEN 'High Value'
        WHEN total_spent >= 5000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS customer_segment
FROM customer_spending
ORDER BY total_spent DESC;


-- ============================================================
-- QUERY 19: CHARGING STATION PERFORMANCE
-- Business Question: Which stations have the highest usage?
-- ============================================================

SELECT
    Station_ID,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Energy_Consumed_kWh), 2) AS total_energy_consumed,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    ROUND(AVG(Session_Duration_Minutes), 2) AS average_duration_minutes
FROM charging_sessions
GROUP BY Station_ID
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 20: ENERGY CONSUMPTION BY CITY
-- Business Question: Which cities consume the most charging energy?
-- ============================================================

SELECT
    City,
    ROUND(SUM(Energy_Consumed_kWh), 2) AS total_energy_consumed,
    ROUND(AVG(Energy_Consumed_kWh), 2) AS average_energy_per_session,
    COUNT(*) AS total_sessions
FROM charging_sessions
GROUP BY City
ORDER BY total_energy_consumed DESC;


-- ============================================================
-- QUERY 21: AVERAGE REVENUE PER SESSION BY CITY
-- Business Question: Which city earns the most per session?
-- ============================================================

SELECT
    City,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    ROUND(AVG(Charging_Cost), 2) AS average_revenue_per_session
FROM charging_sessions
GROUP BY City
ORDER BY average_revenue_per_session DESC;


-- ============================================================
-- QUERY 22: PEAK CHARGING HOURS
-- Business Question: At what hours do customers charge most often?
-- ============================================================

SELECT
    HOUR(Start_Time) AS charging_hour,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue
FROM charging_sessions
GROUP BY HOUR(Start_Time)
ORDER BY total_sessions DESC;


-- ============================================================
-- QUERY 23: REPEAT CUSTOMERS
-- Business Question: How many sessions do returning customers make?
-- ============================================================

SELECT
    Customer_ID,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Charging_Cost), 2) AS total_spent
FROM charging_sessions
GROUP BY Customer_ID
HAVING COUNT(*) > 1
ORDER BY total_sessions DESC, total_spent DESC;


-- ============================================================
-- QUERY 24: RANK STATIONS BY REVENUE
-- Business Question: Which stations are the top revenue generators?
-- ============================================================

SELECT
    Station_ID,
    COUNT(*) AS total_sessions,
    ROUND(SUM(Charging_Cost), 2) AS total_revenue,
    DENSE_RANK() OVER (
        ORDER BY SUM(Charging_Cost) DESC
    ) AS station_rank
FROM charging_sessions
GROUP BY Station_ID
ORDER BY station_rank;


-- ============================================================
-- END OF EV CHARGING STATION ANALYTICS SQL QUERIES
-- ============================================================