--------------------------------------
--	remove trailing spaces
--------------------------------------

--  for deliveries table ---
UPDATE deliveries SET
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

/*
 * Update the single facility identified as having an active service 
 * but missing its 'Site_ID'.
 *
 * -- Background Rationale:--
 * A total of 59 facilities had missing/null SITE_ID values.
 * Cross-referencing with the 'deliveries' table confirmed 58 of these were never served, 
 * justifying their missing 'SITE_ID' values.
- 'Asawinso SDA HSP' was the single exception: it received packages but was missing its 'SITE_ID'.
- The new, valid 'SITE_ID' was sourced directly from the GH2 Zipline Controller Team on 9th Dec, 2025.
*/

-- check to confirm NULL state ---
SELECT FACILITY_NAME, DISTRICT,
       REGION, SITE_ID
       FROM  facilities
       WHERE FACILITY_NAME = 'Asawisno SDA HSP' AND SITE ID IS NULL; --since all blanks were set to NULL initially

-- update 'SITE_ID' as found from Controller Team --
UPDATE facilities
     SET SITE_ID = 1309 --valid site_id from Controller Team
     WHERE FACILITY_NAME = 'Asawinso SDA HSP' AND SITE_ID IS NULL;


-------------------------------------------------
--  update on TIME_ORDER_CONFIRMED_LOCAL column 
-------------------------------------------------
/*
*  Discovered later that some TIME_ORDER_CONFIRMED_LOCAL values were stored
*  as the zero datetime '0000-00-00 00:00:00' instead of NULL.
* This explains why the earlier check
* SELECT * FROM deliveries WHERE TIME_ORDER_CONFIRMED_LOCAL IS NULL;
* returned an empty set even though the column looked blank in the source data.
* 
* Since the dataset is expected to start from 2023‑01‑01, any timestamp
* earlier than 2022‑12‑31 is treated as invalid / missing and should be NULL.
* The following statements implement that assumption and clean the data:
*/

--	Inspect potentially invalid timestamps (including zero dates) ---
SELECT DELIVERY_KEY, HEALTH_FACILITY_NAME, 
	TIME_ORDER_CONFIRMED_LOCAL , TIME_DELIVERED_LOCAL
	FROM deliveries WHERE TIME_ORDER_CONFIRMED_LOCAL < '2023-01-01';

--Convert all such invalid timestamps to NULL so that future checks using
--    TIME_ORDER_CONFIRMED_LOCAL IS NULL correctly identify missing values.
UPDATE deliveries
	SET TIME_ORDER_CONFIRMED_LOCAL = NULL
	WHERE TIME_ORDER_CONFIRMED_LOCAL < '2022-12-31';

------------------------------------
--	check for duplicates ---
------------------------------------
/*
* for 'delivery_key' in deliveries table
* The duplicates identified were found to be valid, as the same delivery key may refer to 
* multiple product deliveries (e.g.one row with Paracetamol, another with Diclofenac Gel).
* These deliveries were part of the same shipment, and no further data cleaning is needed.
* Total number of delivery keys with duplicates: 6188.
*/
SELECT delivery_key, COUNT (*) AS count 
FROM deliveries
GROUP BY delivery_key
HAVING COUNT(*) >1;

-- for facility_id in facilities table
-- returns no duplicate values in this column
SELECT facility_id, COUNT (*) AS count 
FROM facilities
GROUP BY facility_id
HAVING COUNT(*) >1;

---------------------------------
--   Case normalization ---
---------------------------------
--	Deliveries Table ---
-- Check case inconsistency case usage in all VARCHAR/TEXT columns

SELECT PRIORITY AS original_priority,
    LOWER(PRIORITY) AS lowercase_priority,
    COUNT(*) AS count
    FROM deliveries
    GROUP BY PRIORITY 
    ORDER BY count DESC;
-- standardize prority values
UPDATE deliveries 
SET PRIORITY = CASE 
    WHEN LOWER(PRIORITY) = 'emergency' THEN 'Emergency'
    WHEN LOWER(PRIORITY) = 'resupply' THEN 'Resupply'
    WHEN LOWER(PRIORITY) = 'scheduled' THEN 'Scheduled'
    ELSE PRIORITY -- Keeps the original value if no match
END;

SELECT HEALTH_FACILITY_NAME AS original_value, 
	LOWER(HEALTH_FACILITY_NAME) AS normalized_value,
	COUNT(*) AS count 
	FROM deliveries 
	GROUP BY HEALTH_FACILITY_NAME  
	ORDER BY count DESC;

SELECT HEALTH_FACILITY_LOCALITY AS original_value,
	LOWER(HEALTH_FACILITY_LOCALITY ) AS normalized_value,
	COUNT(*) AS count
	FROM deliveries GROUP BY HEALTH_FACILITY_LOCALITY    
	ORDER BY count DESC;

SELECT PRODUCT_NAME  AS original_value, 
	LOWER(PRODUCT_NAME  ) AS normalized_value,
	COUNT(*) AS count
 	FROM deliveries
	GROUP BY PRODUCT_NAME     
	ORDER BY count DESC;

SELECT USE_CASE_CATEGORY AS original_value,
	LOWER(USE_CASE_CATEGORY ) AS normalized_value, 
	COUNT(*) AS count FROM deliveries 
	GROUP BY USE_CASE_CATEGORY  
	ORDER BY count DESC;

SELECT USE_CASE_SUBCATEGORY   AS original_value,
	 LOWER(USE_CASE_SUBCATEGORY ) AS normalized_value,
	 COUNT(*) AS count FROM deliveries
	 GROUP BY USE_CASE_SUBCATEGORY  
	 ORDER BY count DESC;

-------------------------------------------
--	Check for Invalid or Negative Values
--------------------------------------------
-- check for N_UNITS since units delivered can't be negative
SELECT *
	FROM deliveries
	WHERE N_UNITS <= 0;
-- check for invalid SITE_ID values
SELECT *
	FROM facilities
	WHERE SITE_ID <= 0;

--  check for time inconsistencies in delivery and order
--  confirmation time that may cause negative values
--  ignore these in analysis since its return values
--  make up 0.33% of the entire dataset hence insignificant
SELECT *
	FROM deliveries
	WHERE TIME_DELIVERED_LOCAL < TIME_ORDER_CONFIRMED LOCAL;

-- create a view to exclude incorrect times
-- add a delivery duration column
-- further analysis will be in the scope of this view
CREATE VIEW deliveries_valid AS 
	SELECT *, TIMESTAMPDIFF(MINUTE, TIME_ORDER_CONFIRMED_LOCAL, TIME_DELIVERED_LOCAL)
	 AS DELIVERY_DURATION_MINUTES FROM deliveries WHERE TIME_DELIVERED_LOCAL >=  TIME_ORDER_CONFIRMED_LOCAL;






	




