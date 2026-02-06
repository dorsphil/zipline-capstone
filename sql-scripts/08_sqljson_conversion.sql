-- ============================================
--              OVERVIEW PAGE
-- ============================================
-- This file contains queries to generate JSON files
-- for the dashboard  pageS.
-- converts the sql queries to JSON saves output to 
-- corresponding JSON file.
-- ============================================

-- Overview KPIs for dashboard
SELECT JSON_OBJECT(
    'total_deliveries', COUNT(DELIVERY_KEY),
    'total_facilities_served', COUNT(DISTINCT FACILITY_ID),
    'estimated_people_reached',
        SUM(CASE WHEN PRIORITY = 'Emergency' THEN 1 ELSE 0 END)
)
INTO OUTFILE '/var/lib/mysql-files/overview_kpis.json'
FROM deliveries_complete;


-- =========================================
--              IMPACT PAGE
-- =========================================

--  facility coverage
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'facility_type', FACILITY_TYPE,
        'number_of_facilities', number_of_facilities
    )
)
INTO OUTFILE '/var/lib/mysql-files/facilities_by_type.json'
FROM (
    SELECT 
        FACILITY_TYPE,
        COUNT(DISTINCT FACILITY_ID) AS number_of_facilities
    FROM deliveries_complete
    GROUP BY FACILITY_TYPE
) t;

--      regions served
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'region', REGION,
        'delivery_count', delivery_count
    )
)
INTO OUTFILE '/var/lib/mysql-files/deliveries_by_region.json'
FROM (
    SELECT REGION,
           COUNT(*) AS delivery_count
    FROM deliveries_complete
    GROUP BY REGION
    ORDER BY delivery_count DESC
) t;

-- District-level beneficiaries
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'district', DISTRICT,
        'total_deliveries', total_deliveries,
        'pct_of_total_deliveries', pct_of_total_deliveries
    )
)
INTO OUTFILE '/var/lib/mysql-files/deliveries_by_district.json'
FROM (
    SELECT 
        DISTRICT,
        COUNT(*) AS total_deliveries,
        ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM deliveries_complete), 2) AS pct_of_total_deliveries
    FROM deliveries_complete
    GROUP BY DISTRICT
    ORDER BY total_deliveries DESC
) t;

-- Deliveries by facility type
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'facility_type', facility_type,
        'total_deliveries', total_deliveries,
        'pct_of_total_deliveries', pct_of_total_deliveries
    )
)
INTO OUTFILE '/var/lib/mysql-files/deliveries_by_facility_type.json'
FROM (
    SELECT
        f.facility_type,
        COUNT(*) AS total_deliveries,
        ROUND(
            COUNT(*) * 100.0 / (SELECT COUNT(*) FROM deliveries_complete),
            2
        ) AS pct_of_total_deliveries
    FROM deliveries_complete d
    JOIN facilities f
        ON d.facility_id = f.facility_id
    GROUP BY f.facility_type
    ORDER BY total_deliveries DESC
) t;





-- =====================================
--          PRODUCTS PAGE
-- ======================================

-- Products Types Delivered
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'use_case_category', USE_CASE_CATEGORY,
        'total_deliveries', total_deliveries,
        'pct_of_total', pct_of_total
    )
)
INTO OUTFILE '/var/lib/mysql-files/products_by_category.json'
FROM (
    SELECT USE_CASE_CATEGORY,
           COUNT(*) AS total_deliveries,
           ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM deliveries_complete), 2) AS pct_of_total
    FROM deliveries_complete
    GROUP BY USE_CASE_CATEGORY
    ORDER BY total_deliveries DESC
) t;

-- Most Delivered Emergency Product Types
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'use_case_category', USE_CASE_CATEGORY,
        'use_case_subcategory', USE_CASE_SUBCATEGORY,
        'emergency_delivery_count', emergency_delivery_count
    )
)
INTO OUTFILE '/var/lib/mysql-files/emergency_products.json'
FROM (
    SELECT 
        USE_CASE_CATEGORY,
        USE_CASE_SUBCATEGORY,
        COUNT(*) AS emergency_delivery_count
    FROM deliveries_complete
    WHERE PRIORITY = 'Emergency'
    GROUP BY USE_CASE_CATEGORY, USE_CASE_SUBCATEGORY
    ORDER BY emergency_delivery_count DESC
) t;

--  Average Delivery Time by Product Type
SELECT JSON_ARRAYAGG(
    JSON_OBJECT(
        'use_case_category', USE_CASE_CATEGORY,
        'avg_delivery_time_minutes', avg_delivery_time_minutes
    )
)
INTO OUTFILE '/var/lib/mysql-files/avg_delivery_time_by_product.json'
FROM (
    SELECT 
        USE_CASE_CATEGORY,
        ROUND(AVG(DELIVERY_DURATION_MINUTES), 2) AS avg_delivery_time_minutes
    FROM deliveries_complete
    GROUP BY USE_CASE_CATEGORY
    ORDER BY avg_delivery_time_minutes
) t;





