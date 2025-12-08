--------------------------------------
--	remove trailing spaces
--------------------------------------

--  for deliveries table ---
mysql> UPDATE deliveries SET
     NEST_NAME = TRIM(NEST_NAME),
     PRIORITY = TRIM(PRIORITY),
     DELIVERY_KEY = TRIM(DELIVERY_KEY),
     HEALTH_FACILITY_NAME = TRIM(HEALTH_FACILITY_NAME),
     HEALTH_FACILITY_LOCALITY = TRIM(HEALTH_FACILITY_LOCALITY),
     PRODUCT_NAME = TRIM(PRODUCT_NAME),
     USE_CASE_CATEGORY = TRIM(USE_CASE_CATEGORY),
     USE_CASE_SUBCATEGORY = TRIM(USE_CASE_SUBCATEGORY);

-- for facilities table ---
UPDATE facilities SET
     FACILITY_NAME = TRIM(FACILITY_NAME),
     FACILITY_TYPE = TRIM(FACILITY_TYPE),
     DISTRICT = TRIM(DISTRICT),
     REGION = TRIM(REGION);

---------------------------------------
--	check for null values
---------------------------------------


--	for deliveries table ---
SELECT * FROM deliveries WHERE NEST_NAME IS NULL OR TRIM(NEST_NAME) = '';

SELECT * FROM deliveries WHERE PRIORITY IS NULL OR TRIM(PRIORITY) = '';

SELECT * FROM deliveries WHERE DELIVERY_KEY IS NULL OR TRIM(DELIVERY_KEY) = '';

SELECT * FROM deliveries WHERE HEALTH_FACILITY_NAME IS NULL OR TRIM(HEALTH_FACILITY_NAME) = '';

SELECT * FROM deliveries WHERE HEALTH_FACILITY_LOCALITY IS NULL OR TRIM(HEALTH_FACILITY_LOCALITY) = '';

SELECT * FROM deliveries WHERE N_UNITS IS NULL;

SELECT * FROM deliveries WHERE PRODUCT_NAME IS NULL OR TRIM(PRODUCT_NAME) = '';

SELECT * FROM deliveries WHERE USE_CASE_SUBCATEGORY IS NULL OR TRIM(USE_CASE_SUBCATEGORY) = '';

SELECT * FROM deliveries WHERE USE_CASE_CATEGORY IS NULL OR TRIM(USE_CASE_CATEGORY) = '';

SELECT * FROM deliveries WHERE TIME_ORDER_CONFIRMED_LOCAL IS NULL;

SELECT * FROM deliveries WHERE TIME_DELIVERED_LOCAL IS NULL;


-- for facilities table ---
SELECT * FROM facilities WHERE FACILITY_ID IS NULL;

SELECT * FROM facilities WHERE FACILITY_NAME IS NULL OR TRIM(FACILITY_NAME) = '';

SELECT * FROM facilities WHERE FACILITY_TYPE IS NULL OR TRIM(FACILITY_TYPE) = '';

SELECT * FROM facilities WHERE DISTRICT IS NULL OR TRIM(DISTRICT) = '';

SELECT * FROM facilities WHERE REGION IS NULL OR TRIM(REGION) = '';

SELECT * FROM facilities WHERE SITE_ID IS NULL OR SITE_ID = '';


--------------------------------------------
--	   fix null/empty values
--------------------------------------------
- null/empty values were found in only 3 columns of facilities table

-- fix for DISTRICT column(5rows) 
UPDATE facilities 
     SET DISTRICT = 'Unknown'
     WHERE TRIM(DISTRICT) = '' OR DISTRICT IS NULL;

-- fix for REGION column(5rows)
UPDATE facilities
    SET REGION = 'Unknown Region'
    WHERE TRIM(REGION) = '' OR REGION IS NULL;

-- fix for SITE_ID column(59rows)
UPDATE facilities
    SET SITE_ID = NULL
    WHERE SITE_ID = 0;
