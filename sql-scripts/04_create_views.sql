--------------------------------------------------------
-- create a view to join both tables for further analysis
---------------------------------------------------------
-- This view combines:
-- deliveries_valid, the cleaned delivery data (excluding irregular time mismatches)
-- facilities dataset 

CREATE VIEW deliveries_complete AS
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

