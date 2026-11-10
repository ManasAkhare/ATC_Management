"""
Repository of all ADBMS Queries and Operations for ATC Management System.
"""

from typing import List, Tuple, Dict, Any, Optional
from atc_system.db import db_manager

# -----------------------------------------------------------------------------
# FLIGHT OPERATIONS (Relational Core)
# -----------------------------------------------------------------------------

def get_all_flights(search_term: Optional[str] = None, status_filter: Optional[str] = None) -> Tuple[List[Tuple], List[str]]:
    """Fetches flights with optional search and status filter."""
    query = """
        SELECT 
            TRIM(flight_number) AS flight_number,
            TRIM(airline_company) AS airline_company,
            TRIM(departure_airport) AS departure_airport,
            TRIM(arrival_airport) AS arrival_airport,
            passenger_number,
            TRIM(status) AS status
        FROM flight
        WHERE 1=1
    """
    params = []
    if search_term:
        term = f"%{search_term.strip()}%"
        query += """ AND (
            flight_number ILIKE %s OR 
            airline_company ILIKE %s OR 
            departure_airport ILIKE %s OR 
            arrival_airport ILIKE %s
        )"""
        params.extend([term, term, term, term])

    if status_filter and status_filter != "All":
        query += " AND TRIM(status) = %s"
        params.append(status_filter.strip())

    query += " ORDER BY flight_number ASC;"
    return db_manager.execute_query(query, params)

def add_flight(flight_number: str, airline: str, dep_airport: str, arr_airport: str, passengers: int, status: str):
    """Inserts a new flight record."""
    query = """
        INSERT INTO flight (flight_number, airline_company, departure_airport, arrival_airport, passenger_number, status)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    return db_manager.execute_non_query(query, (
        flight_number.strip().upper(),
        airline.strip(),
        dep_airport.strip().upper(),
        arr_airport.strip().upper(),
        int(passengers),
        status.strip()
    ))

def update_flight_status(flight_number: str, new_status: str):
    """Updates the real-time status of a flight."""
    query = "UPDATE flight SET status = %s WHERE flight_number = %s;"
    return db_manager.execute_non_query(query, (new_status.strip(), flight_number.strip()))

def delete_flight(flight_number: str):
    """Deletes a flight and its associated schedule/crew."""
    # Clean up foreign references if necessary
    db_manager.execute_non_query("DELETE FROM schedule WHERE flight_number = %s;", (flight_number,))
    db_manager.execute_non_query("DELETE FROM crew WHERE flight_number = %s;", (flight_number,))
    db_manager.execute_non_query("DELETE FROM user_flight_mapping WHERE flight_number = %s;", (flight_number,))
    query = "DELETE FROM flight WHERE flight_number = %s;"
    return db_manager.execute_non_query(query, (flight_number,))


# -----------------------------------------------------------------------------
# HORIZONTAL FRAGMENTATION (ADBMS Concept 1)
# -----------------------------------------------------------------------------

def get_aircraft_all() -> Tuple[List[Tuple], List[str]]:
    """Returns base aircraft table."""
    query = """
        SELECT 
            TRIM(plane_number) AS plane_number, 
            TRIM(plane_type) AS plane_type, 
            TRIM(manufacturer) AS manufacturer, 
            TRIM(flight_type) AS flight_type 
        FROM aircraft 
        ORDER BY plane_number ASC;
    """
    return db_manager.execute_query(query)

def get_aircraft_commercial() -> Tuple[List[Tuple], List[str]]:
    """Returns horizontal fragment: Commercial aircraft."""
    query = """
        SELECT 
            TRIM(plane_number) AS plane_number, 
            TRIM(plane_type) AS plane_type, 
            TRIM(manufacturer) AS manufacturer, 
            TRIM(flight_type) AS flight_type 
        FROM plane_commercial 
        ORDER BY plane_number ASC;
    """
    return db_manager.execute_query(query)

def get_aircraft_private() -> Tuple[List[Tuple], List[str]]:
    """Returns horizontal fragment: Private aircraft."""
    query = """
        SELECT 
            TRIM(plane_number) AS plane_number, 
            TRIM(plane_type) AS plane_type, 
            TRIM(manufacturer) AS manufacturer, 
            TRIM(flight_type) AS flight_type 
        FROM plane_private 
        ORDER BY plane_number ASC;
    """
    return db_manager.execute_query(query)

def get_reconstructed_horizontal() -> Tuple[List[Tuple], List[str]]:
    """Reconstructs the global relation using UNION ALL of fragments."""
    query = """
        SELECT 
            TRIM(plane_number) AS plane_number, 
            TRIM(plane_type) AS plane_type, 
            TRIM(manufacturer) AS manufacturer, 
            TRIM(flight_type) AS flight_type,
            'Commercial Fragment' AS source_fragment
        FROM plane_commercial
        UNION ALL
        SELECT 
            TRIM(plane_number) AS plane_number, 
            TRIM(plane_type) AS plane_type, 
            TRIM(manufacturer) AS manufacturer, 
            TRIM(flight_type) AS flight_type,
            'Private Fragment' AS source_fragment
        FROM plane_private
        ORDER BY plane_number ASC;
    """
    return db_manager.execute_query(query)

def rebuild_horizontal_fragments():
    """Re-executes the horizontal fragmentation queries on PostgreSQL."""
    q1 = "DROP TABLE IF EXISTS plane_commercial; CREATE TABLE plane_commercial AS SELECT * FROM aircraft WHERE TRIM(flight_type) = 'Commercial';"
    q2 = "DROP TABLE IF EXISTS plane_private; CREATE TABLE plane_private AS SELECT * FROM aircraft WHERE TRIM(flight_type) = 'Private';"
    db_manager.execute_non_query(q1)
    db_manager.execute_non_query(q2)
    return True, "Horizontal fragments (plane_commercial, plane_private) successfully refreshed."


# -----------------------------------------------------------------------------
# VERTICAL FRAGMENTATION (ADBMS Concept 2)
# -----------------------------------------------------------------------------

def get_plane_info() -> Tuple[List[Tuple], List[str]]:
    """Returns vertical fragment 1: plane_info."""
    query = """
        SELECT 
            TRIM(flight_number) AS flight_number, 
            TRIM(airline_company) AS airline_company, 
            passenger_number 
        FROM plane_info 
        ORDER BY flight_number ASC;
    """
    return db_manager.execute_query(query)

def get_route_info() -> Tuple[List[Tuple], List[str]]:
    """Returns vertical fragment 2: route_info."""
    query = """
        SELECT 
            TRIM(flight_number) AS flight_number, 
            TRIM(departure_airport) AS departure_airport, 
            TRIM(arrival_airport) AS arrival_airport, 
            TRIM(status) AS status 
        FROM route_info 
        ORDER BY flight_number ASC;
    """
    return db_manager.execute_query(query)

def get_reconstructed_vertical() -> Tuple[List[Tuple], List[str]]:
    """Reconstructs the global relation via Natural / Inner Join on Flight_Number."""
    query = """
        SELECT 
            p.flight_number,
            p.airline_company,
            p.passenger_number,
            r.departure_airport,
            r.arrival_airport,
            r.status
        FROM plane_info p
        JOIN route_info r ON p.flight_number = r.flight_number
        ORDER BY p.flight_number ASC;
    """
    return db_manager.execute_query(query)

def rebuild_vertical_fragments():
    """Re-executes the vertical fragmentation queries on PostgreSQL."""
    q1 = "DROP TABLE IF EXISTS plane_info; CREATE TABLE plane_info AS SELECT flight_number, airline_company, passenger_number FROM flight;"
    q2 = "DROP TABLE IF EXISTS route_info; CREATE TABLE route_info AS SELECT flight_number, departure_airport, arrival_airport, status FROM flight;"
    db_manager.execute_non_query(q1)
    db_manager.execute_non_query(q2)
    return True, "Vertical fragments (plane_info, route_info) successfully refreshed."


# -----------------------------------------------------------------------------
# AIR TRAFFIC CONTROL SCHEDULE & RUNWAY CONFLICT ENGINE (ADBMS Concept 3)
# -----------------------------------------------------------------------------

def get_all_schedules() -> Tuple[List[Tuple], List[str]]:
    """Fetches schedules joined with flight airline information."""
    query = """
        SELECT 
            s.flight_number,
            COALESCE(TRIM(f.airline_company), 'Unknown') AS airline,
            TO_CHAR(s.departure_time, 'HH24:MI:SS') AS departure_time,
            TO_CHAR(s.arrival_time, 'HH24:MI:SS') AS arrival_time,
            s.runway_number,
            s.terminal_number,
            COALESCE(TRIM(f.status), 'Unknown') AS status
        FROM schedule s
        LEFT JOIN flight f ON s.flight_number = f.flight_number
        ORDER BY s.departure_time ASC;
    """
    return db_manager.execute_query(query)

def check_runway_conflicts(separation_threshold_seconds: int = 900) -> Tuple[List[Tuple], List[str]]:
    """
    ADBMS Operational Query: Identifies safety conflicts where two flights share
    the same runway with less than the separation threshold (e.g. 15 minutes / 900s).
    """
    query = """
        SELECT 
            s1.flight_number AS flight_1,
            s2.flight_number AS flight_2,
            s1.runway_number,
            TO_CHAR(s1.departure_time, 'HH24:MI') AS time_flight_1,
            TO_CHAR(s2.departure_time, 'HH24:MI') AS time_flight_2,
            ROUND(ABS(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time))) / 60) AS separation_mins,
            CASE 
                WHEN ABS(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time))) < 300 THEN 'CRITICAL HAZARD (<5m)'
                ELSE 'WARNING (<15m)'
            END AS conflict_severity
        FROM schedule s1
        JOIN schedule s2 ON s1.runway_number = s2.runway_number 
                         AND s1.flight_number < s2.flight_number
        WHERE ABS(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time))) < %s
        ORDER BY s1.runway_number, s1.departure_time;
    """
    return db_manager.execute_query(query, (separation_threshold_seconds,))

def add_or_update_schedule(flight_num: str, dep_time: str, arr_time: str, runway: int, terminal: str):
    """Inserts or updates a runway schedule."""
    query = """
        INSERT INTO schedule (flight_number, departure_time, arrival_time, runway_number, terminal_number)
        VALUES (%s, %s::time, %s::time, %s, %s)
        ON CONFLICT (flight_number) DO UPDATE
        SET departure_time = EXCLUDED.departure_time,
            arrival_time = EXCLUDED.arrival_time,
            runway_number = EXCLUDED.runway_number,
            terminal_number = EXCLUDED.terminal_number;
    """
    return db_manager.execute_non_query(query, (flight_num, dep_time, arr_time, int(runway), terminal))


# -----------------------------------------------------------------------------
# FLIGHT CREW MANAGEMENT
# -----------------------------------------------------------------------------

def get_all_crew() -> Tuple[List[Tuple], List[str]]:
    """Fetches crew records with flight info."""
    query = """
        SELECT 
            c.crew_id,
            c.flight_number,
            c.crew_size,
            c.pilot,
            c.copilot,
            COALESCE(TRIM(f.airline_company), 'N/A') AS airline
        FROM crew c
        LEFT JOIN flight f ON c.flight_number = f.flight_number
        ORDER BY c.crew_id ASC;
    """
    return db_manager.execute_query(query)


# -----------------------------------------------------------------------------
# SEMI-STRUCTURED DATA & XML DATABASE ENGINE (ADBMS Concept 4)
# -----------------------------------------------------------------------------

def get_raw_xml_documents() -> Tuple[List[Tuple], List[str]]:
    """Fetches stored XML documents from Flight_Data."""
    query = "SELECT id, xml_content::text FROM flight_data ORDER BY id ASC;"
    return db_manager.execute_query(query)

def execute_xpath_query(xpath_expr: str) -> Tuple[List[Tuple], List[str]]:
    """
    Executes PostgreSQL xpath() function on Flight_Data XML content.
    Example: //Flight[Airline="IndiGo"]
    """
    query = "SELECT id, xpath(%s, xml_content)::text[] AS matched_nodes FROM flight_data;"
    return db_manager.execute_query(query, (xpath_expr,))

def get_xmltable_shredded() -> Tuple[List[Tuple], List[str]]:
    """
    Executes PostgreSQL XMLTABLE shredding query: converts XML tree into relational rows.
    """
    query = """
        SELECT xtab.*
        FROM flight_data,
        XMLTABLE('/FlightCatalog/Flight'
            PASSING xml_content
            COLUMNS 
                Flight_No  TEXT PATH 'FlightNumber',
                Airline    TEXT PATH 'Airline',
                From_City  TEXT PATH 'Departure',
                To_City    TEXT PATH 'Arrival',
                Status     TEXT PATH 'Status'
        ) AS xtab;
    """
    return db_manager.execute_query(query)


# -----------------------------------------------------------------------------
# DATABASE SECURITY, RBAC & ROW LEVEL SECURITY (ADBMS Concept 5)
# -----------------------------------------------------------------------------

def get_user_flight_mappings() -> Tuple[List[Tuple], List[str]]:
    """Returns the username-to-flight mappings used for RLS."""
    query = "SELECT username, flight_number FROM user_flight_mapping ORDER BY username, flight_number;"
    return db_manager.execute_query(query)

def add_user_flight_mapping(username: str, flight_number: str):
    """Maps a user to a flight for RLS."""
    query = "INSERT INTO user_flight_mapping (username, flight_number) VALUES (%s, %s) ON CONFLICT DO NOTHING;"
    return db_manager.execute_non_query(query, (username.lower(), flight_number.upper()))

def get_available_roles() -> List[str]:
    """Returns available test roles for demonstration."""
    return ["postgres", "atc", "aditya", "parth", "rajesh", "captain"]


# -----------------------------------------------------------------------------
# ANALYTICS & ATC INSIGHTS (ADBMS Concept 6)
# -----------------------------------------------------------------------------

def get_flight_status_counts() -> List[Tuple[str, int]]:
    """Flight count grouped by status."""
    query = """
        SELECT TRIM(status) AS status, COUNT(*) AS count
        FROM flight
        GROUP BY TRIM(status)
        ORDER BY count DESC;
    """
    rows, _ = db_manager.execute_query(query)
    return rows

def get_airline_distribution() -> List[Tuple[str, int]]:
    """Flight count grouped by airline."""
    query = """
        SELECT TRIM(airline_company) AS airline, COUNT(*) AS count
        FROM flight
        GROUP BY TRIM(airline_company)
        ORDER BY count DESC;
    """
    rows, _ = db_manager.execute_query(query)
    return rows

def get_runway_utilization() -> List[Tuple[int, int]]:
    """Operation count grouped by runway number."""
    query = """
        SELECT runway_number, COUNT(*) AS operations
        FROM schedule
        GROUP BY runway_number
        ORDER BY runway_number ASC;
    """
    rows, _ = db_manager.execute_query(query)
    return rows

def get_passenger_statistics() -> Dict[str, Any]:
    """Summary of passenger statistics."""
    query = """
        SELECT 
            COUNT(*) AS total_flights,
            SUM(passenger_number) AS total_passengers,
            ROUND(AVG(passenger_number), 1) AS avg_passengers,
            MAX(passenger_number) AS max_passengers,
            MIN(passenger_number) AS min_passengers
        FROM flight;
    """
    rows, cols = db_manager.execute_query(query)
    if rows:
        return dict(zip(cols, rows[0]))
    return {}


# -----------------------------------------------------------------------------
# SQL CONSOLE & QUERY PLANNER (EXPLAIN ANALYZE) (ADBMS Concept 7)
# -----------------------------------------------------------------------------

def explain_query(sql_query: str) -> List[str]:
    """Runs EXPLAIN (ANALYZE, BUFFERS) for query performance evaluation."""
    plan_query = f"EXPLAIN (ANALYZE, BUFFERS, VERBOSE) {sql_query.strip().rstrip(';')};"
    rows, _ = db_manager.execute_query(plan_query)
    return [r[0] for r in rows]
