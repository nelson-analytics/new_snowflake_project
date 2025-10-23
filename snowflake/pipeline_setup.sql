-- ======================================================================
-- PROJECT: End-to-End JSON Data Pipeline on Snowflake
-- COMPONENTS: Stage | Snowpipe | Stream | Task | Clean Layer
-- ======================================================================

USE ROLE SYSADMIN;
CREATE DATABASE IF NOT EXISTS PROJ_E2E_DB;
USE DATABASE PROJ_E2E_DB;

-- ======================================================================
-- 1️⃣ CREATE SCHEMAS
-- ======================================================================
CREATE SCHEMA IF NOT EXISTS RAW;
CREATE SCHEMA IF NOT EXISTS CLEAN;

-- ======================================================================
-- 2️⃣ CREATE STAGE (AWS S3)
-- Replace <bucket-name> and <region> accordingly
-- ======================================================================
CREATE OR REPLACE STAGE RAW.json_stage
URL = 's3://<your-s3-bucket-name>/api_data/'
STORAGE_INTEGRATION = aws_integration
FILE_FORMAT = (TYPE = JSON);

-- ======================================================================
-- 3️⃣ CREATE RAW TABLE
-- ======================================================================
CREATE OR REPLACE TABLE RAW.api_events (
  id STRING AUTOINCREMENT START 1 INCREMENT 1,
  payload VARIANT,
  inserted_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ======================================================================
-- 4️⃣ CREATE SNOWPIPE (AUTOMATIC INGESTION)
-- ======================================================================
CREATE OR REPLACE PIPE RAW.pipe_api_events
AUTO_INGEST = TRUE
AS
COPY INTO RAW.api_events (payload)
FROM @RAW.json_stage
FILE_FORMAT = (TYPE = JSON);

-- To monitor pipe status:
-- SHOW PIPES;
-- SELECT SYSTEM$PIPE_STATUS('RAW.pipe_api_events');

-- ======================================================================
-- 5️⃣ CREATE STREAM (TRACK CHANGES IN RAW)
-- ======================================================================
CREATE OR REPLACE STREAM RAW.api_events_stream
ON TABLE RAW.api_events
APPEND_ONLY = TRUE;

-- ======================================================================
-- 6️⃣ CREATE CLEAN TABLE
-- ======================================================================
CREATE OR REPLACE TABLE CLEAN.api_events_clean AS
SELECT
  payload:id::STRING AS event_id,
  payload:timestamp::TIMESTAMP_NTZ AS event_time,
  payload:user_id::STRING AS user_id,
  payload:source::STRING AS source,
  payload:data AS event_data,
  CURRENT_TIMESTAMP() AS load_time
FROM RAW.api_events
WHERE 1=0;

-- ======================================================================
-- 7️⃣ CREATE TRANSFORMATION VIEW (OPTIONAL)
-- ======================================================================
CREATE OR REPLACE VIEW CLEAN.vw_transform_api_events AS
SELECT
  payload:id::STRING AS event_id,
  payload:timestamp::TIMESTAMP_NTZ AS event_time,
  payload:user_id::STRING AS user_id,
  payload:source::STRING AS source,
  payload:data AS event_data,
  CURRENT_TIMESTAMP() AS load_time
FROM RAW.api_events_stream;

-- ======================================================================
-- 8️⃣ CREATE TASK (AUTO TRANSFORMATION EVERY 5 MINUTES)
-- ======================================================================
CREATE OR REPLACE TASK CLEAN.task_load_api_events
  WAREHOUSE = COMPUTE_WH
  SCHEDULE = '5 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('RAW.api_events_stream')
AS
INSERT INTO CLEAN.api_events_clean (event_id, event_time, user_id, source, event_data, load_time)
SELECT event_id, event_time, user_id, source, event_data, load_time
FROM CLEAN.vw_transform_api_events;

-- Activate the Task
ALTER TASK CLEAN.task_load_api_events RESUME;

-- ======================================================================
-- 9️⃣ MONITORING COMMANDS
-- ======================================================================
-- Check if stream has pending data:
-- SELECT SYSTEM$STREAM_HAS_DATA('RAW.api_events_stream');

-- Manually trigger the task (for testing):
-- EXECUTE TASK CLEAN.task_load_api_events;

-- Confirm data load:
-- SELECT * FROM CLEAN.api_events_clean ORDER BY load_time DESC LIMIT 10;

-- ======================================================================
-- ✅ PIPELINE SETUP COMPLETE
-- ======================================================================
