# DELIVERING IMPACT; A DATA-DRIVEN STORY OF ZIPLINE'S VALUE IN GHANA

## PROJECT SUMMARY

**Project Overview**
This project is a data-driven dashboard designed to highlight the operational value, geographic reach
and human impact of Zipline's operations in Ghana.
    
Using synthetic delivery and health facility datasets, the project demonstrates how Zipline’s deliveries 
support health facilities, distribute essential medical products, and respond to life-critical emergencies. 
The final output is a **localhost dashboard website** supported by a robust SQL data-cleaning and analysis pipeline.
    
**Project Objectives**
The project answers three key questions:

**A. Operational Value**
- How many deliveries were made over time?
- What types of products were delivered (e.g., vaccines, blood, essential medicines)?
- Which regions or districts received the most support?

**B. Facility & Geographic Coverage**
- How many health facilities have benefited from these deliveries?
- What types of facilities were supported (clinics, CHPS, hospitals)?
- What level of support was provided to each of the various facility groups (Health Centres,CHPS, Hospitals etc)

**C. Human Impact**
- Assuming that each emergency delivery was for a patient in critical conditions, how many
  lives may have been saved within the period?
- Which communities or districts appear most dependent on Zipline's services?


## TOOLS USED
1. Database: MySQL
2. Query Language: SQL
3. Data Analysis: SQL aggregations and views
4. Frontend: HTML,CSS,JavaScript
5. Visualization: Chart.js
6. Version Control: Git &GitHub


**Data Sources**
Two synthetic datasets were used:

1. Delivery Records
Each row represents a single delivery made to a health facility.

Key fields include:
- Delivery priority (Emergency, Resupply, Scheduled)
- Product category and subcategory
- Order and delivery timestamps
- Number of units delivered
- Facility name and locality

2. Health Facility Data
Each row represents a unique health facility.

Key fields include:
- Facility type (Hospital, Clinic, CHPS, Health Centre)
- District and region
- Delivery site identifier

### DATA CLEANING AND PREPARATION
1. Removed trailing spaces from particular columns

2. Checked and normalize case inconsistencies in text-type data types

3. Checked for null values/ blank spaces and fixed where necessary in all columns.
**SITE_ID NULLS**
Background Rationale:
A total of 59 facilities had missing/null SITE_ID values.
Cross-referencing with the 'deliveries' table confirmed 58 of these were never served, 
justifying their missing 'SITE_ID' values.
'Asawinso SDA HSP' was the single exception: it received packages but was missing its 'SITE_ID'.
The new, valid 'SITE_ID' was sourced directly from the GH2 Zipline Controller Team on 9th Dec, 2025.

````-- check to confirm NULL state ---
SELECT FACILITY_NAME, DISTRICT,
       REGION, SITE_ID
       FROM  facilities
       WHERE FACILITY_NAME = 'Asawisno SDA HSP' AND SITE ID IS NULL; --since all blanks were set to NULL initially

-- update 'SITE_ID' as found from Controller Team --
UPDATE facilities
     SET SITE_ID = 1309 --valid site_id from Controller Team
     WHERE FACILITY_NAME = 'Asawinso SDA HSP' AND SITE_ID IS NULL;
```
**TIME_ORDER_CONFIRMED_LOCAL NULLS**
Discovered later that some TIME_ORDER_CONFIRMED_LOCAL values were stored
as the zero datetime '0000-00-00 00:00:00' instead of NULL.
This explains why the earlier check
```SELECT * FROM deliveries WHERE TIME_ORDER_CONFIRMED_LOCAL IS NULL;
```
returned an empty set even though the column looked blank in the source data.
 Since the dataset is expected to start from 2023‑01‑01, any timestamp
earlier than 2022‑12‑31 is treated as invalid / missing and should be NULL.
The following statements implement that assumption and clean the data:

```--	Inspect potentially invalid timestamps (including zero dates) ---
SELECT DELIVERY_KEY, HEALTH_FACILITY_NAME, 
	TIME_ORDER_CONFIRMED_LOCAL , TIME_DELIVERED_LOCAL
	FROM deliveries WHERE TIME_ORDER_CONFIRMED_LOCAL < '2023-01-01';

--Convert all such invalid timestamps to NULL so that future checks using
--    TIME_ORDER_CONFIRMED_LOCAL IS NULL correctly identify missing values.
UPDATE deliveries
	SET TIME_ORDER_CONFIRMED_LOCAL = NULL
	WHERE TIME_ORDER_CONFIRMED_LOCAL < '2022-12-31';
```
4. Check for duplicates
for 'delivery_key' column in deliveries table
The duplicates identified were found to be valid, as the same delivery key may refer to 
multiple product deliveries (e.g.one row with Paracetamol, another with Diclofenac Gel).
These deliveries were part of the same shipment, and no further data cleaning is needed.
Total number of delivery keys with duplicates: 6188.

````SELECT delivery_key, COUNT (*) AS count 
FROM deliveries
GROUP BY delivery_key
HAVING COUNT(*) >1;

-- for facility_id in facilities table
-- returns no duplicate values in this column
SELECT facility_id, COUNT (*) AS count 
FROM facilities
GROUP BY facility_id
HAVING COUNT(*) >1;
```

5. Check for invalid or negative values
**Timestamp Validation**
131 delivery records (0.33% of total) were found where delivery timestamps occurred before order timestamps. 
These records were treated as data-entry inconsistencies and excluded from analysis.

A cleaned delivery view was created

````CREATE VIEW deliveries_valid AS 
	SELECT *, TIMESTAMPDIFF(MINUTE, TIME_ORDER_CONFIRMED_LOCAL, TIME_DELIVERED_LOCAL)
	 AS DELIVERY_DURATION_MINUTES FROM deliveries WHERE TIME_DELIVERED_LOCAL >=  TIME_ORDER_CONFIRMED_LOCAL;
```

**Data Integration**
To simplify analysis, the cleaned delivery data was joined with facility metadata to create a unified analysis-ready view:
All analysis and dashboard metrics are derived from this unified dataset.

```CREATE VIEW deliveries_complete AS
SELECT
	d.*,
	f.FACILITY_ID,
	f.FACILITY_NAME,
	f. FACILITY_TYPE,
	f.DISTRICT,
	f.REGION,
	f. SITE_ID
FROM deliveries_valid d
INNER JOIN facilities f
ON d.HEALTH_FACILITY_NAME = f.FACILITY_NAME;
```

**Data Pipeline**
````
-----------------------              -----------------------------
| deliveries (raw)     | ------------> | facilities (raw)        |
-----------------------              -----------------------------
               |                           |
               v                           v
        -------------------         -----------------------
        | Clean (deliveries) |       | Clean (facilities)  |
        -------------------         -----------------------
               |                           |
               v                           v
        -------------------         ---------------------------
        | deliveries_valid  | ----> | deliveries_complete     |
        -------------------         ---------------------------
                                            |
                                            v
                                    ---------------------
                                    | Final for Analysis |
                                    ---------------------
```
#### METRICS AND ANALYSIS
The following metrics were computed to address the project objectives:

**Operational Value**
- Total deliveries over time (monthly)
- Total number of valid deliveries
- Product categories(types) delivered
- Regions and Districts receiving the most support
- Average delivery time by product type
- Average delivery time by priority

**Facility & Geographic Coverage**
- Total number of facilities served
- Types of facilities served
- Level of support per facility group, which covered the ff;
    - Deliveries by facility type
    - Priority Distribution by Facility Type
    - Performance(units delivered and product variety)  per Facility Type
    - Minimum and Maximum deliveries per facility within each type
    
**Human Impact**
- Estimated lives saved (count of emergency deliveries)
- Emergency deliveries by district
- Most-delivered emergency product types
- Average emergency response time

**ASSUMPTIONS MADE**
1. Each emergency delivery potentially corresponds to one patient in critical condition, representing a 
   conservative estimate of lives saved.

2. Any facility missing a SITE_ID (59) was checked against delivery records and found not to have received deliveries in 
   2023, except for Asawinso SDA HSP, which had a missing SITE_ID. This was updated after getting the correct information 
   from the GH2 Zipline Controller Team.
   
3. The data is for deliveries from January 1, 2023, onward. Any timestamps before this date or stored as 
   "0000-00-00" were treated as invalid and set to NULL.
   
4. A single DELIVERY_KEY may represent multiple products delivered together in one flight

5. Delivery times show the actual time from order confirmation to delivery completion. Without ETA data, we can't 
   compare actual delivery times to targets, so the focus is on general statistics and patterns instead of performance goals.
   
6. 'Health Facility Locality' in the deliveries table and 'District' in the facilities table are the same 
    thing and are used interchangeably in this analysis.
    
7. Analysis is based on the 'deliveries_complete view'', which includes only records with valid timestamps 
   and combines delivery and facility data.
   
8. Deliveries where delivery time preceded order time (131 records, 0.33% of data) were excluded from analysis as logically invalid.



**Dorsphil Osei Asuming Animwaa**
**Data Analyst Intern**
**Zipline Ghana**


