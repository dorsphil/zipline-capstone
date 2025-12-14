----------------------------------------------
--	Facility & Geographic Coverage
---------------------------------------------


--	Total Number of Facilities Served
SELECT COUNT(DISTINCT FACILITY_ID) AS total_facilities_served
FROM deliveries_complete;


--	Number of Deliveries per Facility Type
SELECT FACILITY_TYPE,
       COUNT(*) AS total_deliveries
FROM deliveries_complete
GROUP BY FACILITY_TYPE
ORDER BY total_deliveries DESC;


--	Level of Support per Facility Group
------------------------------------------------

-- 	Deliveries Per Facility Type
SELECT 
    FACILITY_TYPE,
    COUNT(*) AS total_deliveries,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM deliveries_complete), 2) AS pct_of_total_deliveries,
    COUNT(DISTINCT FACILITY_ID) AS facilities_served,
    ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT FACILITY_ID), 2) AS avg_deliveries_per_facility
FROM deliveries_complete
GROUP BY FACILITY_TYPE
ORDER BY total_deliveries DESC;

--	Priority Distribution by Facility Type
SELECT 
    FACILITY_TYPE,
    COUNT(*) AS total_deliveries,
  
    SUM(CASE WHEN PRIORITY = 'Emergency' THEN 1 ELSE 0 END) AS emergency_deliveries,
    ROUND(SUM(CASE WHEN PRIORITY = 'Emergency' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_emergency,
   
    SUM(CASE WHEN PRIORITY = 'Resupply' THEN 1 ELSE 0 END) AS resupply_deliveries,
    ROUND(SUM(CASE WHEN PRIORITY = 'Resupply' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_resupply,
    
    SUM(CASE WHEN PRIORITY = 'Scheduled' THEN 1 ELSE 0 END) AS scheduled_deliveries,
    ROUND(SUM(CASE WHEN PRIORITY = 'Scheduled' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS pct_scheduled
FROM deliveries_complete
GROUP BY FACILITY_TYPE
ORDER BY total_deliveries DESC;

--	Performance(units delivered and product variety)  per Facility Type
SELECT 
    FACILITY_TYPE,
    COUNT(*) AS total_deliveries,
    SUM(N_UNITS) AS total_units_delivered,
    ROUND(AVG(N_UNITS), 2) AS avg_units_per_delivery,
    COUNT(DISTINCT PRODUCT_NAME) AS product_variety
FROM deliveries_complete
GROUP BY FACILITY_TYPE
ORDER BY total_deliveries DESC;

--	Minimum and Maximum deliveries per facility within each type
SELECT 
    FACILITY_TYPE,
    MIN(delivery_count) AS min_deliveries_per_facility,
    MAX(delivery_count) AS max_deliveries_per_facility,
    ROUND(AVG(delivery_count), 2) AS avg_deliveries_per_facility
FROM (
    SELECT 
        FACILITY_TYPE,
        FACILITY_ID,
        COUNT(*) AS delivery_count
    FROM deliveries_complete
    GROUP BY FACILITY_TYPE, FACILITY_ID
) AS facility_delivery_counts
GROUP BY FACILITY_TYPE
ORDER BY max_deliveries_per_facility DESC;
