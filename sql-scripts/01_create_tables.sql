--create database
CREATE DATABASE zipline_db;
USE zipline_db; --switches to use created database

--create table for Deliveries.csv
CREATE TABLE deliveries (
         NEST_NAME VARCHAR(100),
         PRIORITY VARCHAR(50),
         DELIVERY_KEY VARCHAR(50),
         HEALTH_FACILITY_NAME VARCHAR(255),
         HEALTH_FACILITY_LOCALITY VARCHAR(255),
         N_UNITS INT,
         PRODUCT_NAME VARCHAR(255),
         USE_CASE_CATEGORY VARCHAR(255),
         USE_CASE_SUBCATEGORY VARCHAR(255),
         TIME_ORDER_CONFIRMED_LOCAL DATETIME,
         TIME_DELIVERED_LOCAL DATETIME
     );

--create tables for health_facility_records.csv
CREATE TABLE facilities (
     FACILITY_ID INT,
     FACILITY_NAME VARCHAR(255),
     FACILITY_TYPE VARCHAR(255),
     DISTRICT VARCHAR(255),
     REGION VARCHAR(255),
     SITE_ID INT
     );



