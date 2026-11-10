# ✈ Air Traffic Control (ATC) Management System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/PostgreSQL-15%20%7C%2016%20%7C%2018-336791.svg)](https://www.postgresql.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter%20%2F%20TTK-06b6d4.svg)]()
[![Offline](https://img.shields.io/badge/Mode-100%25%20Offline-success.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()

An enterprise-grade, offline desktop application and Air Traffic Control operations simulator built in **Python (Tkinter/TTK)** connected to a **PostgreSQL** database designed originally in **pgAdmin 4**.

This project implements all core and advanced concepts of an **Advanced Database Management System (ADBMS)** course, including **Horizontal and Vertical Fragmentation**, **Semi-Structured XML Processing & XPath Evaluation**, **XMLTABLE Relational Shredding**, **Role-Based Access Control (RBAC)**, **PostgreSQL Row-Level Security (RLS)**, and **Runway Safety Conflict Detection**.

---

## 📸 Key Features & ADBMS Modules

### 1. ✈ Live Flights Monitor & Relational CRUD
* Real-time flight tracking across commercial airlines (IndiGo, Air India, SpiceJet, Vistara, Akasa Air, etc.) and private aviation fleets.
* Interactive filters by status (`On-Time`, `Delayed`, `Boarding`, `Scheduled`, `Cancelled`) and live full-text search across flight numbers, airlines, and airports.
* Complete transactional CRUD with real-time status updates and constraint checks.

### 2. 🏢 Horizontal Fragmentation & Lossless Reconstruction (ADBMS Concept 1)
* **Fragmentation Predicates**:
  * $\text{Fragment } 1 \ (plane\_commercial): \sigma_{Flight\_Type = 'Commercial'}(Aircraft)$
  * $\text{Fragment } 2 \ (plane\_private): \sigma_{Flight\_Type = 'Private'}(Aircraft)$
* **Reconstruction**: Full lossless reassembly using `UNION ALL`.
* **Dynamic Rebuilding**: Re-executes fragmentation queries directly on the live PostgreSQL server.

### 3. 🔀 Vertical Fragmentation & Lossless Join Decomposition (ADBMS Concept 2)
* **Fragmentation Attributes**:
  * $\text{Fragment } 1 \ (plane\_info): \Pi_{Flight\_Number, Airline\_Company, Passenger\_Number}(Flight)$
  * $\text{Fragment } 2 \ (route\_info): \Pi_{Flight\_Number, Departure\_Airport, Arrival\_Airport, Status}(Flight)$
* **Reconstruction**: Lossless Join Decomposition reconstructed via Natural Join / Inner Join on the primary key `Flight_Number` ($R = R_1 \bowtie_{Flight\_Number} R_2$).

### 4. 🛫 ATC Runway Scheduling & Safety Conflict Radar (ADBMS Concept 3)
* Master timeline of runway allocations and gate/terminal assignments.
* **Automated Runway Conflict Detection Engine**: Evaluates time intervals between aircraft scheduled on identical runways. Automatically flags hazards violating the minimum separation buffer ($< 15\text{ minutes}$ warning, $< 5\text{ minutes}$ critical hazard).

### 5. 👨‍✈️ Flight Crew & Pilot Rostering
* Roster management matching aircraft captains (Pilot-in-Command), first officers (Co-Pilot), and total crew size to scheduled flight routes.

### 6. 📄 Semi-Structured Data & Native XML Engine (ADBMS Concept 4)
* **XML Storage**: Direct storage of hierarchical `FlightCatalog` documents inside PostgreSQL `XML` type columns.
* **XPath Query Terminal**: Live evaluation of native PostgreSQL `xpath()` expressions (e.g., `//Flight[Airline="IndiGo"]`, `//Flight[Departure="BOM"]`, `//Flight[Status="Delayed"]`).
* **XMLTABLE Relational Shredder**: Transforms nested, hierarchical XML documents into relational 2D tuples directly inside PostgreSQL.

### 7. 🛡 Database Security, RBAC & Row-Level Security (RLS) (ADBMS Concept 5)
* Fine-grained access control using PostgreSQL native security roles: `admin`, `atc`, `passenger`, `captain`.
* **Row-Level Security (RLS) Policy Demonstration**:
  ```sql
  CREATE POLICY passenger_mapping_policy ON flight
  FOR SELECT TO passenger
  USING (flight_number IN (
      SELECT flight_number FROM user_flight_mapping 
      WHERE username = CURRENT_USER
  ));
  ```
* Live dynamic role switcher: Test the application as `postgres` (sees all flights), or switch session to passenger users (`aditya` or `parth`) and observe PostgreSQL's database engine automatically restrict visible rows strictly to their mapped flights.

### 8. 📊 Operations Analytics & KPI Center
* High-level executive KPI cards: Monitored flights, passenger volume, on-time rate, and active runways.
* Native canvas-rendered visual distributions of flight statuses, airline shares, and runway slot utilization.

### 9. 💻 Interactive SQL Query Console & EXPLAIN ANALYZE (ADBMS Concept 6)
* In-app SQL editor with pre-loaded ADBMS experiment presets.
* Execution plan analyzer running `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` to demonstrate query execution cost, buffer hits, and B-Tree index scans (`idx_status`, `idx_departure_time`, `idx_flight_num`).
* One-click CSV data export.

---

## 📁 Repository Structure

```
ATC Management/
├── atc_system/                   # Application Core Package
│   ├── __init__.py
│   ├── config.py                 # Configuration and environment loaders
│   ├── db.py                     # PostgreSQL connection manager & query executor
│   ├── queries.py                # All ADBMS queries (CRUD, Joins, XML, RLS, Analytics)
│   └── ui/                       # Modern Desktop GUI (Tkinter/TTK)
│       ├── __init__.py
│       ├── theme.py              # Aviation Command Center dark theme
│       ├── app.py                # Main application window & navigation sidebar
│       ├── connection_dialog.py  # Runtime database credentials dialog
│       ├── flights_view.py       # Live flights monitor & CRUD
│       ├── aircraft_view.py      # Horizontal fragmentation view
│       ├── vertical_frag_view.py # Vertical fragmentation view
│       ├── schedule_view.py      # Runway scheduling & conflict detector
│       ├── crew_view.py          # Flight crew roster
│       ├── xml_data_view.py      # XML catalog & XPath processor
│       ├── security_view.py      # RBAC & Row-Level Security demo
│       ├── analytics_view.py     # Operations dashboard & charts
│       └── query_console.py      # Interactive SQL editor & EXPLAIN ANALYZE
├── database/                     # Database Scripts
│   ├── schema.sql                # Complete database schema, sample dataset, indexes & RLS
│   ├── adbms_queries.sql         # Documented SQL queries for all ADBMS lab experiments
│   └── setup_db.py               # Automated 1-click database initialization script
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore file for Python, PostgreSQL, and OS
├── requirements.txt              # Python dependencies
├── run.py                        # Main entry point to launch the application
└── README.md                     # Documentation
```

---

## 🚀 Quickstart Guide

### Prerequisites
1. **Python 3.10+** (includes Tkinter)
2. **PostgreSQL** (running locally on port 5432, accessible via pgAdmin 4 or psql)

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/atc-management-system.git
cd "atc-management-system"
```

---

### Step 2: Set Up Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

---

### Step 3: Configure Database Credentials
Copy `.env.example` to `.env`:
```bash
# Windows
copy .env.example .env

# Linux / macOS
cp .env.example .env
```
Open `.env` in any text editor and update your PostgreSQL credentials if different:
```ini
DB_HOST=127.0.0.1
DB_PORT=5432
DB_NAME=Airport
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

---

### Step 4: Initialize the Database (One-Click)
Run the automated database setup script to create the `Airport` database, all tables, initial dataset (50 aircraft, 50 flights, 50 schedules, 50 crew members), indexes, and security roles:
```bash
python database/setup_db.py
```

---

### Step 5: Launch the Application
Start the offline desktop GUI:
```bash
python run.py
```

---

## 📤 How to Upload This Project to GitHub

Follow these steps from the root directory of this project:

```bash
# 1. Initialize git repository
git init

# 2. Stage all project files (ignoring temporary files via .gitignore)
git add .

# 3. Create your initial commit
git commit -m "Initial commit: Air Traffic Control (ATC) Management System ADBMS project"

# 4. Rename main branch
git branch -M main

# 5. Link your GitHub remote repository (replace with your repo URL)
git remote add origin https://github.com/your-username/atc-management-system.git

# 6. Push to GitHub
git push -u origin main
```

---

## 🛠 Technologies Used
* **Programming Language**: Python 3.12
* **Database Engine**: PostgreSQL (tested on v15, v16, v18)
* **Database Driver**: `psycopg2-binary`
* **Desktop GUI**: Python Tkinter with TTK custom modern styling
* **Architecture**: Model-View-Controller (MVC) separation of concerns
* **Offline Execution**: 100% offline, zero internet or cloud dependencies

---

## 📜 License
This project is open-source and available under the [MIT License](LICENSE).
