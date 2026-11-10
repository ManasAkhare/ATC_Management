"""
Interactive ADBMS SQL Query Console & Execution Plan Analyzer.
Allows executing custom SQL queries and visualizing EXPLAIN ANALYZE query plans.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from atc_system.db import db_manager
from atc_system import queries
from atc_system.ui.theme import *

PRESET_QUERIES = [
    (
        "1. Horizontal Fragmentation Reconstruction (UNION ALL)",
        "SELECT plane_number, plane_type, manufacturer, flight_type, 'Commercial' AS fragment\nFROM plane_commercial\nUNION ALL\nSELECT plane_number, plane_type, manufacturer, flight_type, 'Private' AS fragment\nFROM plane_private\nORDER BY plane_number;"
    ),
    (
        "2. Vertical Fragmentation Lossless Natural Join",
        "SELECT p.flight_number, p.airline_company, p.passenger_number, r.departure_airport, r.arrival_airport, r.status\nFROM plane_info p\nJOIN route_info r ON p.flight_number = r.flight_number\nORDER BY p.flight_number;"
    ),
    (
        "3. XMLTABLE Relational Shredder",
        "SELECT xtab.*\nFROM flight_data,\nXMLTABLE('/FlightCatalog/Flight'\n    PASSING xml_content\n    COLUMNS \n        Flight_No  TEXT PATH 'FlightNumber',\n        Airline    TEXT PATH 'Airline',\n        From_City  TEXT PATH 'Departure',\n        To_City    TEXT PATH 'Arrival',\n        Status     TEXT PATH 'Status'\n) AS xtab;"
    ),
    (
        "4. Native XPath Query for IndiGo Flights",
        "SELECT id, xpath('//Flight[Airline=\"IndiGo\"]', xml_content) AS indigo_nodes\nFROM flight_data;"
    ),
    (
        "5. ATC Runway Minimum Separation Conflict Detection (<15 mins)",
        "SELECT \n    s1.flight_number AS f1, \n    s2.flight_number AS f2, \n    s1.runway_number, \n    s1.departure_time AS t1, \n    s2.departure_time AS t2,\n    ROUND(ABS(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time))) / 60) AS gap_mins\nFROM schedule s1\nJOIN schedule s2 ON s1.runway_number = s2.runway_number AND s1.flight_number < s2.flight_number\nWHERE ABS(EXTRACT(EPOCH FROM (s2.departure_time - s1.departure_time))) < 900\nORDER BY s1.runway_number, gap_mins;"
    ),
    (
        "6. Airline Delay Statistics & Percentage",
        "SELECT \n    TRIM(airline_company) AS airline,\n    COUNT(*) AS total_flights,\n    SUM(CASE WHEN TRIM(status) = 'Delayed' THEN 1 ELSE 0 END) AS delayed_count,\n    ROUND(100.0 * SUM(CASE WHEN TRIM(status) = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS delay_pct,\n    SUM(passenger_number) AS total_pax\nFROM flight\nGROUP BY airline_company\nORDER BY total_flights DESC;"
    ),
    (
        "7. Full Operations: Flight + Schedule + Crew Assignment",
        "SELECT \n    f.flight_number, f.airline_company, f.departure_airport, f.arrival_airport, f.status,\n    s.departure_time, s.runway_number, s.terminal_number,\n    c.pilot, c.crew_size\nFROM flight f\nLEFT JOIN schedule s ON f.flight_number = s.flight_number\nLEFT JOIN crew c ON f.flight_number = c.flight_number\nORDER BY s.departure_time NULLS LAST;"
    ),
    (
        "8. Session Security Audit: Current User & Permissions",
        "SELECT CURRENT_USER, SESSION_USER, current_database();"
    )
]

class QueryConsoleView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()

    def _build_ui(self):
        # Top Preset Bar
        preset_frame = ttk.Frame(self, style="Panel.TFrame", padding=10)
        preset_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(preset_frame, text="Load ADBMS Query Preset:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT, padx=(0, 10))

        preset_names = [p[0] for p in PRESET_QUERIES]
        self.preset_cb = ttk.Combobox(preset_frame, values=preset_names, state="readonly", width=50, style="TCombobox")
        self.preset_cb.set("Select a pre-crafted ADBMS query...")
        self.preset_cb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.preset_cb.bind("<<ComboboxSelected>>", self._on_preset_selected)

        ttk.Button(preset_frame, text="Load Preset", style="Cyan.TButton", command=self._load_current_preset).pack(side=tk.RIGHT)

        # SQL Editor Area
        editor_frame = ttk.Frame(self, style="Panel.TFrame", padding=10)
        editor_frame.pack(fill=tk.X, padx=10, pady=5)

        lbl_row = ttk.Frame(editor_frame, style="Panel.TFrame")
        lbl_row.pack(fill=tk.X, pady=(0, 4))
        ttk.Label(lbl_row, text="SQL Query Editor:", font=FONT_HEADING, style="Panel.TLabel").pack(side=tk.LEFT)
        ttk.Label(lbl_row, text="Press Ctrl+Enter to Execute", style="Secondary.TLabel").pack(side=tk.RIGHT)

        self.txt_query = tk.Text(
            editor_frame,
            bg="#111c33",
            fg="#f8fafc",
            insertbackground="#ffffff",
            font=FONT_MONO,
            height=6,
            wrap="none",
            borderwidth=0,
            padx=8,
            pady=8
        )
        self.txt_query.pack(fill=tk.X)
        self.txt_query.insert("1.0", "SELECT * FROM flight LIMIT 20;")
        self.txt_query.bind("<Control-Return>", lambda e: self.run_query())

        btn_row = ttk.Frame(editor_frame, style="Panel.TFrame")
        btn_row.pack(fill=tk.X, pady=(8, 0))

        ttk.Button(btn_row, text="▶ Run Query", style="Success.TButton", command=self.run_query).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row, text="⚡ EXPLAIN ANALYZE (Execution Plan)", style="Warning.TButton", command=self.explain_query).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row, text="Export CSV", style="TButton", command=self.export_csv).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="Clear Editor", style="TButton", command=lambda: self.txt_query.delete("1.0", tk.END)).pack(side=tk.RIGHT)

        # Results Notebook: Table vs Query Plan
        self.res_notebook = ttk.Notebook(self)
        self.res_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

        # Tab 1: Data Table
        self.tab_table = ttk.Frame(self.res_notebook, style="Panel.TFrame", padding=10)
        self.res_notebook.add(self.tab_table, text="Query Results (Table)")

        self.tree_res = ttk.Treeview(self.tab_table, show="headings", selectmode="browse")
        self.vsb = ttk.Scrollbar(self.tab_table, orient="vertical", command=self.tree_res.yview)
        self.hsb = ttk.Scrollbar(self.tab_table, orient="horizontal", command=self.tree_res.xview)
        self.tree_res.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

        self.tree_res.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Tab 2: Execution Plan
        self.tab_plan = ttk.Frame(self.res_notebook, style="Panel.TFrame", padding=10)
        self.res_notebook.add(self.tab_plan, text="Execution Plan (EXPLAIN ANALYZE)")

        self.txt_plan = tk.Text(
            self.tab_plan,
            bg="#111c33",
            fg="#a7f3d0",
            insertbackground="#ffffff",
            font=FONT_MONO,
            wrap="none",
            borderwidth=0,
            padx=10,
            pady=10
        )
        plan_vsb = ttk.Scrollbar(self.tab_plan, orient="vertical", command=self.txt_plan.yview)
        self.txt_plan.configure(yscrollcommand=plan_vsb.set)
        self.txt_plan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        plan_vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.current_rows = []
        self.current_cols = []

    def _on_preset_selected(self, event):
        self._load_current_preset()

    def _load_current_preset(self):
        idx = self.preset_cb.current()
        if idx >= 0 and idx < len(PRESET_QUERIES):
            sql = PRESET_QUERIES[idx][1]
            self.txt_query.delete("1.0", tk.END)
            self.txt_query.insert("1.0", sql)

    def run_query(self):
        sql = self.txt_query.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Query editor is empty.", parent=self)
            return

        try:
            rows, cols = db_manager.execute_query(sql)
            self.current_rows = rows
            self.current_cols = cols

            # Clear treeview
            for item in self.tree_res.get_children():
                self.tree_res.delete(item)

            if not cols:
                self.tree_res["columns"] = ("status",)
                self.tree_res.heading("status", text="Result")
                self.tree_res.insert("", tk.END, values=(f"Query executed successfully. ({len(rows)} rows)",))
            else:
                self.tree_res["columns"] = cols
                for col in cols:
                    self.tree_res.heading(col, text=col)
                    self.tree_res.column(col, width=130, anchor="w")

                for r in rows:
                    self.tree_res.insert("", tk.END, values=[str(v) if v is not None else "NULL" for v in r])

            self.res_notebook.select(self.tab_table)

        except Exception as e:
            messagebox.showerror("Query Error", f"SQL execution failed:\n\n{e}", parent=self)

    def explain_query(self):
        sql = self.txt_query.get("1.0", tk.END).strip()
        if not sql:
            messagebox.showwarning("Warning", "Query editor is empty.", parent=self)
            return

        try:
            plan_lines = queries.explain_query(sql)
            self.txt_plan.delete("1.0", tk.END)
            self.txt_plan.insert("1.0", f"-- EXPLAIN (ANALYZE, BUFFERS, VERBOSE)\n-- Query: {sql}\n" + ("=" * 70) + "\n\n")
            for line in plan_lines:
                self.txt_plan.insert(tk.END, line + "\n")

            self.res_notebook.select(self.tab_plan)

        except Exception as e:
            messagebox.showerror("Explain Error", f"Failed to generate query execution plan:\n\n{e}", parent=self)

    def export_csv(self):
        if not self.current_rows or not self.current_cols:
            messagebox.showwarning("Export Warning", "No query results to export.", parent=self)
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Save Query Results as CSV",
            parent=self
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.current_cols)
                writer.writerows(self.current_rows)
            messagebox.showinfo("Export Success", f"Successfully exported {len(self.current_rows)} rows to:\n{file_path}", parent=self)
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write CSV:\n{e}", parent=self)
