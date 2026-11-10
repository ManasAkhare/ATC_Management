-- ============================================================================
-- ADVANCED DATABASE MANAGEMENT SYSTEMS (ADBMS)
-- PROJECT: AIR TRAFFIC CONTROL (ATC) MANAGEMENT SYSTEM
-- SCRIPT: ALL ADBMS QUERIES & LAB DEMONSTRATIONS
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. HORIZONTAL FRAGMENTATION
-- Concept: Splitting a relation horizontally into subsets of tuples based
--          on selection predicates (Flight_Type).
-- ----------------------------------------------------------------------------

-- Create Horizontal Fragment 1: Commercial Aircraft
DROP TABLE IF EXISTS plane_commercial;
CREATE TABLE plane_commercial AS
SELECT * FROM aircraft
WHERE flight_type = 'Commercial';

-- Create Horizontal Fragment 2: Private / General Aviation Aircraft
DROP TABLE IF EXISTS plane_private;
CREATE TABLE plane_private AS
SELECT * FROM aircraft
WHERE flight_type = 'Private';

-- Reconstruction of Horizontal Fragments (Completeness & Reconstructibility Rule):
SELECT * FROM plane_commercial
UNION ALL
SELECT * FROM plane_private;


-- ----------------------------------------------------------------------------
-- 2. VERTICAL FRAGMENTATION
-- Concept: Splitting a relation vertically into subsets of attributes with
--          a common primary key for lossless decomposition.
-- ----------------------------------------------------------------------------

-- Create Vertical Fragment 1: Airplane / Fleet Details
DROP TABLE IF EXISTS plane_info;
CREATE TABLE plane_info AS
SELECT flight_number, airline_company, passenger_number
FROM flight;

-- Create Vertical Fragment 2: Route & Operational Status
DROP TABLE IF EXISTS route_info;
CREATE TABLE route_info AS
SELECT flight_number, departure_airport, arrival_airport, status
FROM flight;

-- Lossless Reconstruction of Vertical Fragments via Natural Join on Flight_Number:
SELECT 
    p.flight_number,
    p.airline_company,
    p.passenger_number,
    r.departure_airport,
    r.arrival_airport,
    r.status
FROM plane_info p
JOIN route_info r ON p.flight_number = r.flight_number;


-- ----------------------------------------------------------------------------
-- 3. SEMI-STRUCTURED DATA & XML DATABASE PROCESSING
-- Concept: Storing, indexing, and querying hierarchical XML data with XPath
--          and relational shredding via XMLTABLE.
-- ----------------------------------------------------------------------------

-- Table definition for XML documents
CREATE TABLE IF NOT EXISTS Flight_Data (
    id SERIAL PRIMARY KEY,
    xml_content XML
);

-- XPath Query 1: Extract flights belonging to 'IndiGo'
SELECT xpath('//Flight[Airline="IndiGo"]', xml_content) 
FROM Flight_Data;

-- XPath Query 2: Extract flights departing from Mumbai ('BOM')
SELECT xpath('//Flight[Departure="BOM"]', xml_content) 
FROM Flight_Data;

-- XPath Query 3: Extract flight numbers with status 'Delayed'
SELECT xpath('//Flight[Status="Delayed"]/FlightNumber/text()', xml_content)
FROM Flight_Data;

-- XML Shredding using XMLTABLE (Transform hierarchical XML to relational tuples):
SELECT xtab.*
FROM Flight_Data,
XMLTABLE('/FlightCatalog/Flight'
    PASSING xml_content
    COLUMNS 
        Flight_No  TEXT PATH 'FlightNumber',
        Airline    TEXT PATH 'Airline',
        From_City  TEXT PATH 'Departure',
        To_City    TEXT PATH 'Arrival',
        Status     TEXT PATH 'Status'
) AS xtab;


-- ----------------------------------------------------------------------------
-- 4. DATABASE SECURITY, ROLES & ROW LEVEL SECURITY (RLS)
-- Concept: Fine-grained access control using PostgreSQL roles, grants, and RLS.
-- ----------------------------------------------------------------------------

-- Role creation
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'admin') THEN
        CREATE ROLE admin;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'atc') THEN
        CREATE ROLE atc;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'passenger') THEN
        CREATE ROLE passenger;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'captain') THEN
        CREATE ROLE captain WITH PASSWORD '123' LOGIN;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'aditya') THEN
        CREATE ROLE aditya WITH PASSWORD '123' LOGIN IN ROLE passenger;
    END IF;
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'parth') THEN
        CREATE ROLE parth WITH PASSWORD '123' LOGIN IN ROLE passenger;
    END IF;
END $$;

-- Enable Row Level Security (RLS)
ALTER TABLE flight ENABLE ROW LEVEL SECURITY;
ALTER TABLE flight FORCE ROW LEVEL SECURITY;

-- Policy: Passengers can ONLY view flights mapped to their specific username
DROP POLICY IF EXISTS passenger_mapping_policy ON flight;
CREATE POLICY passenger_mapping_policy ON flight
FOR SELECT TO passenger
USING (
    flight_number IN (
        SELECT flight_number 
        FROM user_flight_mapping 
        WHERE username = CURRENT_USER
    )
);

-- Test RLS as user 'aditya' (Should only see flight '6E2134'):
SET ROLE aditya;
SELECT CURRENT_USER;
SELECT * FROM flight;
RESET ROLE;

-- Test RLS as user 'parth' (Should only see flight 'SG123'):
SET ROLE parth;
SELECT CURRENT_USER;
SELECT * FROM flight;
RESET ROLE;


-- ----------------------------------------------------------------------------
-- 5. INDEXING & QUERY OPTIMIZATION (EXPLAIN ANALYZE)
-- Concept: Evaluating cost, execution time, and buffer hits with B-Tree indexes.
-- ----------------------------------------------------------------------------

-- Create Indexes
CREATE INDEX IF NOT EXISTS idx_status ON flight USING btree (status);
CREATE INDEX IF NOT EXISTS idx_departure_time ON schedule USING btree (departure_time);
CREATE INDEX IF NOT EXISTS idx_flight_num ON flight USING btree (flight_number);

-- Query with EXPLAIN ANALYZE to show index scan
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM flight WHERE status = 'Delayed';

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM schedule WHERE departure_time BETWEEN '06:00:00' AND '12:00:00';


-- ----------------------------------------------------------------------------
-- 6. AIR TRAFFIC CONTROL OPERATIONAL QUERIES
-- ----------------------------------------------------------------------------

-- ATC Runway Conflict Detection:
-- Identifies flights sharing the same runway with overlapping departure times (< 15 mins)
SELECT 
    s1.flight_number AS flight_1,
    s2.flight_number AS flight_2,
    s1.runway_number,
    s1.departure_time AS flight_1_departure,
    s2.departure_time AS flight_2_departure,
    ROUND(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time)) / 60) AS separation_minutes
FROM schedule s1
JOIN schedule s2 ON s1.runway_number = s2.runway_number 
                 AND s1.flight_number < s2.flight_number
WHERE ABS(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time))) < 900
ORDER BY s1.runway_number, s1.departure_time;

-- Flight Overview with Crew and Runway Assignment:
SELECT 
    f.flight_number,
    f.airline_company,
    f.departure_airport,
    f.arrival_airport,
    f.passenger_number,
    f.status,
    s.departure_time,
    s.arrival_time,
    s.runway_number,
    s.terminal_number,
    c.pilot,
    c.copilot
FROM flight f
LEFT JOIN schedule s ON f.flight_number = s.flight_number
LEFT JOIN crew c ON f.flight_number = c.flight_number
ORDER BY s.departure_time NULLS LAST;

-- Runway Utilization Statistics:
SELECT 
    runway_number,
    COUNT(*) AS total_scheduled_operations,
    MIN(departure_time) AS first_operation,
    MAX(departure_time) AS last_operation
FROM schedule
GROUP BY runway_number
ORDER BY total_scheduled_operations DESC;

-- Airline Performance & Delay Statistics:
SELECT 
    airline_company,
    COUNT(*) AS total_flights,
    SUM(CASE WHEN TRIM(status) = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count,
    ROUND(100.0 * SUM(CASE WHEN TRIM(status) = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS delay_rate_percent,
    SUM(passenger_number) AS total_passengers
FROM flight
GROUP BY airline_company
ORDER BY total_flights DESC;
