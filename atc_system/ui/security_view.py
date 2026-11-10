"""
Database Security, RBAC & Row Level Security (RLS) Simulation View (ADBMS Concept 5).
Demonstrates PostgreSQL Fine-Grained Access Control, Dynamic Role Switching,
and Row Level Security policies based on user_flight_mapping.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system.db import db_manager
from atc_system import queries
from atc_system.ui.theme import *

class SecurityView(ttk.Frame):
    def __init__(self, parent, on_role_changed_callback=None):
        super().__init__(parent, style="TFrame")
        self.on_role_changed_callback = on_role_changed_callback
        self._build_ui()
        self.refresh_all()

    def _build_ui(self):
        # Header Info Banner
        info_panel = ttk.Frame(self, style="Panel.TFrame", padding=12)
        info_panel.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(info_panel, text="ADBMS Concept: Role-Based Access Control (RBAC) & Row Level Security (RLS)", font=FONT_SUBTITLE, style="Subtitle.TLabel").pack(anchor="w")
        desc = (
            "Row-Level Security (RLS) restricts which rows of a table can be selected or modified depending on the active PostgreSQL role.\n"
            "• Policy: CREATE POLICY passenger_mapping_policy ON flight FOR SELECT TO passenger\n"
            "          USING (flight_number IN (SELECT flight_number FROM user_flight_mapping WHERE username = CURRENT_USER));\n"
            "• Demo: When active role is 'aditya', the DB engine strictly returns only flight 6E2134. When 'parth', only flight SG123."
        )
        ttk.Label(info_panel, text=desc, style="Secondary.TLabel", justify="left").pack(anchor="w", pady=(4, 0))

        # Role Selector Control Bar
        role_bar = ttk.Frame(self, style="Panel.TFrame", padding=10)
        role_bar.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(role_bar, text="Simulate Active Session Role:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT, padx=(0, 10))

        self.roles = queries.get_available_roles()
        for rname in self.roles:
            btn_style = "Success.TButton" if rname == "postgres" else "Cyan.TButton"
            btn = ttk.Button(role_bar, text=f"Role: {rname}", style=btn_style, command=lambda r=rname: self._switch_role(r))
            btn.pack(side=tk.LEFT, padx=3)

        self.active_role_badge = ttk.Label(role_bar, text="Active Role: postgres", font=FONT_HEADING, foreground="#38bdf8", style="Panel.TLabel")
        self.active_role_badge.pack(side=tk.RIGHT, padx=10)

        # Split pane: Left is Visible Flights under RLS, Right is user_flight_mapping table
        split_pane = ttk.Frame(self, style="TFrame")
        split_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left: Visible Flights under RLS (65%)
        left_frame = ttk.Frame(split_pane, style="Panel.TFrame", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.rls_title = ttk.Label(left_frame, text="Rows Visible to Current Role via 'SELECT * FROM flight':", font=FONT_HEADING, style="Panel.TLabel")
        self.rls_title.pack(anchor="w", pady=(0, 6))

        cols = ("flight_number", "airline_company", "departure_airport", "arrival_airport", "passenger_number", "status")
        self.tree_rls = ttk.Treeview(left_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_rls.heading("flight_number", text="Flight No")
        self.tree_rls.heading("airline_company", text="Airline")
        self.tree_rls.heading("departure_airport", text="Origin")
        self.tree_rls.heading("arrival_airport", text="Destination")
        self.tree_rls.heading("passenger_number", text="Passengers")
        self.tree_rls.heading("status", text="Status")

        self.tree_rls.column("flight_number", width=90, anchor="center")
        self.tree_rls.column("airline_company", width=140, anchor="w")
        self.tree_rls.column("departure_airport", width=90, anchor="center")
        self.tree_rls.column("arrival_airport", width=90, anchor="center")
        self.tree_rls.column("passenger_number", width=90, anchor="center")
        self.tree_rls.column("status", width=110, anchor="center")

        vsb_rls = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree_rls.yview)
        self.tree_rls.configure(yscrollcommand=vsb_rls.set)
        self.tree_rls.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_rls.pack(side=tk.RIGHT, fill=tk.Y)

        # Right: User Flight Mapping & Assignment (35%)
        right_frame = ttk.Frame(split_pane, style="Panel.TFrame", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))

        ttk.Label(right_frame, text="RLS Mapping Table (user_flight_mapping):", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 6))

        m_cols = ("username", "flight_number")
        self.tree_map = ttk.Treeview(right_frame, columns=m_cols, show="headings", height=8)
        self.tree_map.heading("username", text="Username")
        self.tree_map.heading("flight_number", text="Mapped Flight No")
        self.tree_map.column("username", width=120, anchor="center")
        self.tree_map.column("flight_number", width=120, anchor="center")

        vsb_m = ttk.Scrollbar(right_frame, orient="vertical", command=self.tree_map.yview)
        self.tree_map.configure(yscrollcommand=vsb_m.set)
        self.tree_map.pack(fill=tk.X, pady=(0, 10))

        # Add Mapping form
        ttk.Separator(right_frame, orient="horizontal").pack(fill=tk.X, pady=6)
        ttk.Label(right_frame, text="Add User-Flight Mapping:", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 4))

        form = ttk.Frame(right_frame, style="Panel.TFrame")
        form.pack(fill=tk.X)

        ttk.Label(form, text="Username (Role):", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(anchor="w")
        self.ent_user = ttk.Entry(form, style="TEntry")
        self.ent_user.pack(fill=tk.X, pady=(0, 4))

        ttk.Label(form, text="Flight Number:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(anchor="w")
        self.ent_flight = ttk.Entry(form, style="TEntry")
        self.ent_flight.pack(fill=tk.X, pady=(0, 8))

        ttk.Button(form, text="+ Add Mapping Rule", style="Success.TButton", command=self._add_mapping).pack(fill=tk.X)

    def refresh_all(self):
        self.refresh_mappings()
        self.refresh_rls_table()

    def refresh_mappings(self):
        try:
            rows, _ = queries.get_user_flight_mappings()
            for item in self.tree_map.get_children():
                self.tree_map.delete(item)
            for r in rows:
                self.tree_map.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load user flight mappings:\n{e}", parent=self)

    def refresh_rls_table(self):
        cur_role = db_manager.get_current_role()
        self.active_role_badge.config(text=f"Active Role: {cur_role}")
        self.rls_title.config(text=f"Rows Visible to Role '{cur_role}' via 'SELECT * FROM flight':")

        try:
            rows, _ = queries.get_all_flights()
            for item in self.tree_rls.get_children():
                self.tree_rls.delete(item)
            for r in rows:
                self.tree_rls.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to execute RLS flight query for role {cur_role}:\n{e}", parent=self)

    def _switch_role(self, role_name: str):
        success, msg = db_manager.set_role(role_name)
        if success:
            self.refresh_rls_table()
            if self.on_role_changed_callback:
                self.on_role_changed_callback(role_name)
        else:
            messagebox.showerror("Role Error", msg, parent=self)

    def _add_mapping(self):
        u = self.ent_user.get().strip().lower()
        f = self.ent_flight.get().strip().upper()
        if not (u and f):
            messagebox.showwarning("Validation", "Both username and flight number are required.", parent=self)
            return

        try:
            queries.add_user_flight_mapping(u, f)
            messagebox.showinfo("Success", f"Mapped user '{u}' to flight '{f}'!", parent=self)
            self.ent_user.delete(0, tk.END)
            self.ent_flight.delete(0, tk.END)
            self.refresh_mappings()
            self.refresh_rls_table()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add mapping:\n{e}", parent=self)
