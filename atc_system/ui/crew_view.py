"""
Flight Crew and Pilot Roster Management View.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system import queries
from atc_system.ui.theme import *

class CrewView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()
        self.refresh_data()

    def _build_ui(self):
        # Header Control Panel
        control_panel = ttk.Frame(self, style="Panel.TFrame", padding=10)
        control_panel.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(control_panel, text="Search Crew / Pilot:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(control_panel, textvariable=self.search_var, width=25, style="TEntry")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.filter_data())

        ttk.Button(control_panel, text="Refresh", style="Cyan.TButton", command=self.refresh_data).pack(side=tk.RIGHT, padx=5)

        # Table Panel
        table_frame = ttk.Frame(self, style="Panel.TFrame", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        cols = ("crew_id", "flight_number", "crew_size", "pilot", "copilot", "airline")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings", selectmode="browse")

        self.tree.heading("crew_id", text="Crew ID")
        self.tree.heading("flight_number", text="Assigned Flight")
        self.tree.heading("crew_size", text="Total Crew")
        self.tree.heading("pilot", text="Captain (Pilot-in-Command)")
        self.tree.heading("copilot", text="First Officer (Co-Pilot)")
        self.tree.heading("airline", text="Airline Company")

        self.tree.column("crew_id", width=90, anchor="center")
        self.tree.column("flight_number", width=110, anchor="center")
        self.tree.column("crew_size", width=90, anchor="center")
        self.tree.column("pilot", width=220, anchor="w")
        self.tree.column("copilot", width=220, anchor="w")
        self.tree.column("airline", width=150, anchor="w")

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Status Bar
        bottom_bar = ttk.Frame(self, style="Panel.TFrame", padding=8)
        bottom_bar.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.count_label = ttk.Label(bottom_bar, text="Total Crew Rosters: 0", style="Secondary.TLabel")
        self.count_label.pack(side=tk.LEFT)

        self.all_rows = []

    def refresh_data(self):
        try:
            self.all_rows, _ = queries.get_all_crew()
            self.filter_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load crew assignments:\n{e}", parent=self)

    def filter_data(self):
        query = self.search_var.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        matched = 0
        for r in self.all_rows:
            crew_id, fnum, csize, pilot, copilot, airline = r
            if not query or any(query in str(field).lower() for field in [crew_id, fnum, pilot, copilot, airline]):
                self.tree.insert("", tk.END, values=r)
                matched += 1

        self.count_label.config(text=f"Total Crew Rosters: {len(self.all_rows)} (Showing: {matched})")
