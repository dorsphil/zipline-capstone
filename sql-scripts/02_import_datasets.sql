-- mysql --local-infile=1 -u root -p zipline_db (run in terminal to connect to MySQL with local infile enabled)

-- enable LOCAL INFILE globally(for all connections)
SET GLOBAL local_infile = 1;

-- import Deliveries.csv file
-- maps csv columns directly to deliveries table colums

LOAD DATA LOCAL INFILE '/home/dorsphil/Desktop/zipline-capstone/data/Deliveries.csv'
     INTO TABLE deliveries
     FIELDS TERMINATED BY ',' 
     ENCLOSED BY '"'
     LINES TERMINATED BY '\n'
     IGNORE 1 ROWS --skips header row
     (NEST_NAME, PRIORITY, DELIVERY_KEY, HEALTH_FACILITY_NAME, HEALTH_FACILITY_LOCALITY, 
     N_UNITS, PRODUCT_NAME, USE_CASE_CATEGORY, USE_CASE_SUBCATEGORY, 
     TIME_ORDER_CONFIRMED_LOCAL, TIME_DELIVERED_LOCAL);

-- import health_facility_records.csv
-- maps csv columns directly to facilities table columns

LOAD DATA LOCAL INFILE '/home/dorsphil/Desktop/zipline-capstone/data/health_facility_records.csv'
     INTO TABLE facilities
     FIELDS TERMINATED BY ',' 
     ENCLOSED BY '"'
     LINES TERMINATED BY '\n'
     IGNORE 1 ROWS --skips header row
     (FACILITY_ID, FACILITY_NAME, FACILITY_TYPE, DISTRICT, REGION, SITE_ID);

