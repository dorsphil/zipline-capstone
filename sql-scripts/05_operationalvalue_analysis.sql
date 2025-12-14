--------------------------------------------
--	Total Deliveries Made Over Time
--------------------------------------------
SELECT DATE_FORMAT(TIME_ORDER_CONFIRMED_LOCAL, '%Y-%m') AS month,
       COUNT(*) AS total_deliveries
FROM deliveries_full
GROUP BY month
ORDER BY month;

-------------------------------------------
--	Product Types Delivered
-------------------------------------------
SELECT USE_CASE_CATEGORY,
	COUNT(*) AS total_deliveries,
	ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM deliveries_complete), 2) AS pct_of_total
FROM deliveries_complete
GROUP BY USE_CASE_CATEGORY
ORDER BY total_deliveries DESC;

------------------------------------------
--Regions/Districts Receiving Most Support
------------------------------------------

-- Per Regions
SELECT REGION,
       COUNT(*) AS delivery_count
FROM deliveries_full
GROUP BY REGION
ORDER BY delivery_count DESC;

-- Per District
SELECT DISTRICT,
       COUNT(*) AS delivery_count
FROM deliveries_full
GROUP BY DISTRICT
ORDER BY delivery_count DESC;


----------------------------------------------
--	Average Delivery Time by Product Type
---------------------------------------------
SELECT 
    USE_CASE_CATEGORY,
    ROUND(AVG(DELIVERY_DURATION_MINUTES), 2) AS avg_delivery_time_minutes
FROM deliveries_complete
GROUP BY USE_CASE_CATEGORY
ORDER BY avg_delivery_time_minutes;

-------------------------------------------
--	Average Delivery Time by Priority
-------------------------------------------
-- Average delivery time by priority (operational efficiency)
SELECT 
    PRIORITY,
    ROUND(AVG(DELIVERY_DURATION_MINUTES), 2) AS avg_delivery_time_min
FROM deliveries_complete
GROUP BY PRIORITY
ORDER BY avg_delivery_time_min;
