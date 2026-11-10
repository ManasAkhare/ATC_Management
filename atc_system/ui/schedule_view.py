"""
ATC Runway Scheduling & Safety Conflict Radar View (ADBMS Concept 3).
Features real-time schedule management and automated runway collision / separation
conflict detection algorithms.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system import queries
from atc_system.ui.theme import *

class ScheduleView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()
        self.refresh_all()

    def _build_ui(self):
        # Conflict Alert Banner / Header
        self.conflict_banner = ttk.Frame(self, style="Panel.TFrame", padding=12)
        self.conflict_banner.pack(fill=tk.X, padx=10, pady=(10, 5))

        banner_top = ttk.Frame(self.conflict_banner, style="Panel.TFrame")
        banner_top.pack(fill=tk.X)
        self.conflict_title = ttk.Label(banner_top, text="ATC Runway Safety & Conflict Engine", font=FONT_SUBTITLE, style="Subtitle.TLabel")
        self.conflict_title.pack(side=tk.LEFT)

        ttk.Button(banner_top, text="Run Conflict Scan", style="Cyan.TButton", command=self.scan_conflicts).pack(side=tk.RIGHT)

        self.conflict_desc = ttk.Label(
            self.conflict_banner, 
            text="Scanning runway allocations for minimum separation violations (< 15 minutes buffer between movements on identical runway)...",
            style="Secondary.TLabel"
        )
        self.conflict_desc.pack(anchor="w", pady=(4, 0))

        # Main horizontal split: Left is Schedule Table, Right is Conflict Radar & Form
        content_frame = ttk.Frame(self, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left: Schedule Table (70% width)
        left_frame = ttk.Frame(content_frame, style="Panel.TFrame", padding=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        ttk.Label(left_frame, text="Active Runway & Terminal Allocations", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 8))

        cols = ("flight_number", "airline", "departure_time", "arrival_time", "runway_number", "terminal_number", "status")
        self.tree_sched = ttk.Treeview(left_frame, columns=cols, show="headings", selectmode="browse")

        self.tree_sched.heading("flight_number", text="Flight No")
        self.tree_sched.heading("airline", text="Airline")
        self.tree_sched.heading("departure_time", text="Departure (IST)")
        self.tree_sched.heading("arrival_time", text="Arrival (IST)")
        self.tree_sched.heading("runway_number", text="Runway")
        self.tree_sched.heading("terminal_number", text="Terminal")
        self.tree_sched.heading("status", text="Status")

        self.tree_sched.column("flight_number", width=85, anchor="center")
        self.tree_sched.column("airline", width=120, anchor="w")
        self.tree_sched.column("departure_time", width=105, anchor="center")
        self.tree_sched.column("arrival_time", width=105, anchor="center")
        self.tree_sched.column("runway_number", width=70, anchor="center")
        self.tree_sched.column("terminal_number", width=75, anchor="center")
        self.tree_sched.column("status", width=95, anchor="center")

        vsb_sched = ttk.Scrollbar(left_frame, orient="vertical", command=self.tree_sched.yview)
        self.tree_sched.configure(yscrollcommand=vsb_sched.set)
        self.tree_sched.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_sched.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_sched.bind("<<TreeviewSelect>>", self._on_schedule_selected)

        # Right: Conflict Alerts & Slot Assignment Form (30% width)
        right_frame = ttk.Frame(content_frame, style="Panel.TFrame", padding=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))

        ttk.Label(right_frame, text="Detected Runway Conflicts (<15 min)", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 5))

        conf_cols = ("f1", "f2", "rwy", "sep", "sev")
        self.tree_conflicts = ttk.Treeview(right_frame, columns=conf_cols, show="headings", height=6)
        self.tree_conflicts.heading("f1", text="Flight 1")
        self.tree_conflicts.heading("f2", text="Flight 2")
        self.tree_conflicts.heading("rwy", text="Rwy")
        self.tree_conflicts.heading("sep", text="Gap (m)")
        self.tree_conflicts.heading("sev", text="Severity")

        self.tree_conflicts.column("f1", width=65, anchor="center")
        self.tree_conflicts.column("f2", width=65, anchor="center")
        self.tree_conflicts.column("rwy", width=45, anchor="center")
        self.tree_conflicts.column("sep", width=55, anchor="center")
        self.tree_conflicts.column("sev", width=110, anchor="center")

        self.tree_conflicts.tag_configure("CRITICAL", foreground="#ef4444")
        self.tree_conflicts.tag_configure("WARNING", foreground="#f59e0b")

        self.tree_conflicts.pack(fill=tk.X, pady=(0, 10))

        # Update / Assign Slot Form
        ttk.Separator(right_frame, orient="horizontal").pack(fill=tk.X, pady=8)
        ttk.Label(right_frame, text="Assign / Update Runway Slot", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 6))

        form_frame = ttk.Frame(right_frame, style="Panel.TFrame")
        form_frame.pack(fill=tk.X)

        fields = [
            ("Flight Number:", "flight_num"),
            ("Departure Time (HH:MM:SS):", "dep_time"),
            ("Arrival Time (HH:MM:SS):", "arr_time"),
            ("Runway Number (e.g. 9, 14, 28):", "runway"),
            ("Terminal (e.g. T1, T2, T3):", "terminal"),
        ]

        self.form_entries = {}
        for lbl_text, key in fields:
            ttk.Label(form_frame, text=lbl_text, style="Panel.TLabel", font=FONT_BODY_BOLD).pack(anchor="w", pady=(2, 0))
            entry = ttk.Entry(form_frame, style="TEntry")
            entry.pack(fill=tk.X, pady=(0, 4))
            self.form_entries[key] = entry

        ttk.Button(form_frame, text="Save Runway Slot", style="Success.TButton", command=self._save_slot).pack(fill=tk.X, pady=(8, 0))

    def refresh_all(self):
        self.refresh_schedules()
        self.scan_conflicts()

    def refresh_schedules(self):
        try:
            rows, _ = queries.get_all_schedules()
            for item in self.tree_sched.get_children():
                self.tree_sched.delete(item)
            for r in rows:
                self.tree_sched.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load schedules:\n{e}", parent=self)

    def scan_conflicts(self):
        try:
            rows, _ = queries.check_runway_conflicts(separation_threshold_seconds=900)
            for item in self.tree_conflicts.get_children():
                self.tree_conflicts.delete(item)

            crit_count = 0
            for r in rows:
                f1, f2, rwy, t1, t2, sep, sev = r
                tag = "CRITICAL" if "CRITICAL" in sev else "WARNING"
                if tag == "CRITICAL":
                    crit_count += 1
                self.tree_conflicts.insert("", tk.END, values=(f1, f2, rwy, sep, sev), tags=(tag,))

            if rows:
                self.conflict_title.config(text=f"ATC Runway Safety Engine: {len(rows)} Conflicts Flagged!")
                self.conflict_desc.config(
                    text=f"WARNING: Found {len(rows)} flight pairs violating minimum runway separation time (< 15 mins). {crit_count} are critical hazard (< 5 mins)."
                )
            else:
                self.conflict_title.config(text="ATC Runway Safety Engine: All Runways Clear")
                self.conflict_desc.config(text="No conflicting departures scheduled within 15 minutes of each other on shared runways.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to scan runway conflicts:\n{e}", parent=self)

    def _on_schedule_selected(self, event):
        selected = self.tree_sched.selection()
        if not selected:
            return
        vals = self.tree_sched.item(selected[0])["values"]
        # vals: flight_number, airline, departure_time, arrival_time, runway_number, terminal_number, status
        self.form_entries["flight_num"].delete(0, tk.END)
        self.form_entries["flight_num"].insert(0, vals[0])

        self.form_entries["dep_time"].delete(0, tk.END)
        self.form_entries["dep_time"].insert(0, vals[2])

        self.form_entries["arr_time"].delete(0, tk.END)
        self.form_entries["arr_time"].insert(0, vals[3])

        self.form_entries["runway"].delete(0, tk.END)
        self.form_entries["runway"].insert(0, vals[4])

        self.form_entries["terminal"].delete(0, tk.END)
        self.form_entries["terminal"].insert(0, vals[5])

    def _save_slot(self):
        fnum = self.form_entries["flight_num"].get().strip().upper()
        dep = self.form_entries["dep_time"].get().strip()
        arr = self.form_entries["arr_time"].get().strip()
        rwy = self.form_entries["runway"].get().strip()
        term = self.form_entries["terminal"].get().strip().upper()

        if not (fnum and dep and arr and rwy and term):
            messagebox.showerror("Validation", "Please fill in all runway slot fields.", parent=self)
            return

        try:
            rwy_num = int(rwy)
        except ValueError:
            messagebox.showerror("Validation", "Runway must be a valid number.", parent=self)
            return

        try:
            queries.add_or_update_schedule(fnum, dep, arr, rwy_num, term)
            messagebox.showinfo("Success", f"Runway slot for {fnum} saved successfully!", parent=self)
            self.refresh_all()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to save schedule:\n{e}", parent=self)
