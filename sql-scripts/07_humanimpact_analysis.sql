---------------------------------------------
--	Human Impact
---------------------------------------------

--  Estimated Lives Saved
SELECT 
    COUNT(*) AS estimated_lives_saved,
FROM deliveries_complete
WHERE PRIORITY = 'Emergency';

--	Communities/Districts Most Dependent on Zipline

-- The source data uses 'Health Facility Locality' and 'District' 
-- interchangeably to refer to the same administrative divisions.
SELECT 
    DISTRICT,
    COUNT(*) AS total_deliveries,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM deliveries_complete), 2) AS pct_of_total_deliveries
FROM deliveries_complete
GROUP BY DISTRICT
ORDER BY total_deliveries DESC; 


----------------------------------------------
--	Most Delivered Emergency Product Types
----------------------------------------------
SELECT 
    USE_CASE_CATEGORY,
    USE_CASE_SUBCATEGORY,
    COUNT(*) AS emergency_delivery_count
FROM deliveries_complete
WHERE PRIORITY = 'Emergency'
GROUP BY USE_CASE_CATEGORY, USE_CASE_SUBCATEGORY
ORDER BY emergency_delivery_count DESC;


--------------------------------------------
--	Emergency Response Speed by Region
--------------------------------------------
SELECT 
    REGION,
    ROUND(AVG(DELIVERY_DURATION_MINUTES ), 2) AS avg_emergency_response_time
FROM deliveries_complete
WHERE PRIORITY = 'Emergency'
GROUP BY REGION
ORDER BY avg_emergency_response_time;


