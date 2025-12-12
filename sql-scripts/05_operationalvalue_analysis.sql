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
	COUNT(*) AS total_deliveries
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

