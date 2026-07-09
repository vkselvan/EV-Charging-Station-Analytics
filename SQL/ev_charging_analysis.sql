-- EV Charging Station Analytics Project
-- SQL Analysis Queries


-- Select Database
USE ev_charging;


-- 1. Total Charging Sessions

SELECT 
COUNT(*) AS total_sessions
FROM charging_sessions;



-- 2. Total Revenue Generated

SELECT
SUM(Charging_Cost) AS total_revenue
FROM charging_sessions;



-- 3. Average Charging Cost

SELECT
AVG(Charging_Cost) AS average_cost
FROM charging_sessions;



-- 4. Revenue by City

SELECT

City,

SUM(Charging_Cost) AS total_revenue

FROM charging_sessions

GROUP BY City

ORDER BY total_revenue DESC;



-- 5. Charging Sessions by City

SELECT

City,

COUNT(Session_ID) AS total_sessions

FROM charging_sessions

GROUP BY City

ORDER BY total_sessions DESC;



-- 6. Top 10 Customers by Spending

SELECT TOP 10
	Customer_ID,
	SUM(Charging_Cost) AS total_spent
FROM charging_sessions
GROUP BY Customer_ID
ORDER BY total_spent DESC;



-- 7. EV Manufacturer Performance

SELECT

Manufacturer,

COUNT(Session_ID) AS total_sessions,

SUM(Charging_Cost) AS total_revenue

FROM charging_sessions

GROUP BY Manufacturer

ORDER BY total_revenue DESC;



-- 8. Charger Type Analysis

SELECT

Charger_Type,

COUNT(Session_ID) AS total_sessions,

SUM(Charging_Cost) AS total_revenue,

AVG(Charging_Cost) AS average_cost

FROM charging_sessions

GROUP BY Charger_Type;



-- 9. Payment Method Analysis

SELECT

Payment_Method,

COUNT(Session_ID) AS transactions,

SUM(Charging_Cost) AS revenue

FROM charging_sessions

GROUP BY Payment_Method

ORDER BY revenue DESC;



-- 10. Vehicle Model Performance

SELECT

Vehicle_Model,

SUM(Energy_Consumed_kWh) AS total_energy,

SUM(Charging_Cost) AS revenue

FROM charging_sessions

GROUP BY Vehicle_Model

ORDER BY revenue DESC;



-- 11. Monthly Revenue Trend
SELECT
	MONTH(Start_Time) AS month,
	SUM(Charging_Cost) AS revenue
FROM charging_sessions
GROUP BY MONTH(Start_Time)
ORDER BY month;


-- 12. Monthly Charging Sessions

SELECT

MONTH(Start_Time) AS month,

COUNT(Session_ID) AS sessions

FROM charging_sessions

GROUP BY MONTH(Start_Time)

ORDER BY month;



-- 13. City Revenue Ranking

SELECT

City,

SUM(Charging_Cost) AS revenue,

RANK() OVER(
ORDER BY SUM(Charging_Cost) DESC
) AS city_rank

FROM charging_sessions

GROUP BY City;



-- 14. Customer Ranking

SELECT

Customer_ID,

SUM(Charging_Cost) AS total_spent,

DENSE_RANK() OVER(
ORDER BY SUM(Charging_Cost) DESC
) AS customer_rank

FROM charging_sessions

GROUP BY Customer_ID;



-- 15. Top Vehicles by Manufacturer

WITH vehicle_rank AS
(
SELECT

Manufacturer,

Vehicle_Model,

SUM(Charging_Cost) AS revenue,

ROW_NUMBER() OVER(
PARTITION BY Manufacturer
ORDER BY SUM(Charging_Cost) DESC
) AS rank_no

FROM charging_sessions

GROUP BY Manufacturer, Vehicle_Model
)

SELECT *

FROM vehicle_rank

WHERE rank_no <= 3;



-- 16. Revenue Growth using LAG

WITH monthly_revenue AS
(
SELECT

MONTH(Start_Time) AS month,

SUM(Charging_Cost) AS revenue

FROM charging_sessions

GROUP BY MONTH(Start_Time)
)

SELECT

month,

revenue,

LAG(revenue) OVER(
ORDER BY month
) AS previous_month,

revenue -
LAG(revenue) OVER(
ORDER BY month
) AS growth

FROM monthly_revenue;



-- 17. Running Total Revenue

WITH monthly_revenue AS
(
SELECT

MONTH(Start_Time) AS month,

SUM(Charging_Cost) AS revenue

FROM charging_sessions

GROUP BY MONTH(Start_Time)
)

SELECT

month,

revenue,

SUM(revenue) OVER(
ORDER BY month
) AS running_total

FROM monthly_revenue;



-- 18. Customer Segmentation

WITH customer_data AS
(
SELECT

Customer_ID,

SUM(Charging_Cost) AS total_spent

FROM charging_sessions

GROUP BY Customer_ID
)

SELECT

Customer_ID,

total_spent,

CASE

WHEN total_spent >= 10000
THEN 'High Value'

WHEN total_spent >= 5000
THEN 'Medium Value'

ELSE 'Low Value'

END AS category

FROM customer_data;



-- 19. Station Performance

SELECT

Station_ID,

COUNT(Session_ID) AS sessions,

SUM(Charging_Cost) AS revenue

FROM charging_sessions

GROUP BY Station_ID

ORDER BY revenue DESC;



-- 20. City Energy Consumption

SELECT

City,

SUM(Energy_Consumed_kWh) AS total_energy,

COUNT(Session_ID) AS sessions

FROM charging_sessions

GROUP BY City

ORDER BY total_energy DESC;