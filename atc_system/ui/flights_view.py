"""
Flights Management View.
Provides full CRUD, search, and real-time status updates for the relational flight relation.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system import queries
from atc_system.ui.theme import *

class AddFlightDialog(tk.Toplevel):
    def __init__(self, parent, on_save_callback):
        super().__init__(parent)
        self.title("Add New Flight")
        self.geometry("420x340")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()

        self.on_save_callback = on_save_callback
        self._build_ui()
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"+{x}+{y}")

    def _build_ui(self):
        container = ttk.Frame(self, style="Panel.TFrame", padding=15)
        container.pack(fill=tk.BOTH, expand=True, padx=12, pady=12)

        ttk.Label(container, text="Register New Flight", font=FONT_SUBTITLE, style="Subtitle.TLabel").pack(anchor="w", pady=(0, 10))

        self.entries = {}
        fields = [
            ("Flight Number:", "flight_number", "e.g. 6E9901"),
            ("Airline Company:", "airline", "e.g. IndiGo"),
            ("Departure Airport:", "dep_airport", "e.g. DEL"),
            ("Arrival Airport:", "arr_airport", "e.g. BOM"),
            ("Passenger Count:", "passengers", "180"),
        ]

        for label_text, key, placeholder in fields:
            row = ttk.Frame(container, style="Panel.TFrame")
            row.pack(fill=tk.X, pady=3)
            ttk.Label(row, text=label_text, width=16, style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT)
            entry = ttk.Entry(row, style="TEntry")
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.entries[key] = entry

        # Status Combobox
        row = ttk.Frame(container, style="Panel.TFrame")
        row.pack(fill=tk.X, pady=3)
        ttk.Label(row, text="Initial Status:", width=16, style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT)
        self.status_cb = ttk.Combobox(row, values=["Scheduled", "On-Time", "Boarding", "Delayed", "Cancelled"], state="readonly", style="TCombobox")
        self.status_cb.set("Scheduled")
        self.status_cb.pack(side=tk.RIGHT, fill=tk.X, expand=True)

        btn_row = ttk.Frame(container, style="Panel.TFrame")
        btn_row.pack(fill=tk.X, pady=(15, 0))
        ttk.Button(btn_row, text="Cancel", style="TButton", command=self.destroy).pack(side=tk.LEFT)
        ttk.Button(btn_row, text="Save Flight", style="Success.TButton", command=self._save).pack(side=tk.RIGHT)

    def _save(self):
        flight_num = self.entries["flight_number"].get().strip().upper()
        airline = self.entries["airline"].get().strip()
        dep = self.entries["dep_airport"].get().strip().upper()
        arr = self.entries["arr_airport"].get().strip().upper()
        pax_str = self.entries["passengers"].get().strip()
        status = self.status_cb.get().strip()

        if not (flight_num and airline and dep and arr and pax_str):
            messagebox.showerror("Validation Error", "All fields are required.", parent=self)
            return

        try:
            pax = int(pax_str)
            if pax < 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Passenger count must be a non-negative integer.", parent=self)
            return

        try:
            queries.add_flight(flight_num, airline, dep, arr, pax, status)
            messagebox.showinfo("Success", f"Flight {flight_num} registered successfully!", parent=self)
            self.on_save_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add flight:\n{e}", parent=self)


class FlightsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()
        self.refresh_data()

    def _build_ui(self):
        # Top Controls Bar
        control_panel = ttk.Frame(self, style="Panel.TFrame", padding=10)
        control_panel.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(control_panel, text="Search Flights:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(control_panel, textvariable=self.search_var, width=22, style="TEntry")
        self.search_entry.pack(side=tk.LEFT, padx=(0, 15))
        self.search_entry.bind("<Return>", lambda e: self.refresh_data())

        ttk.Label(control_panel, text="Filter Status:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT, padx=(0, 5))
        self.status_filter_cb = ttk.Combobox(control_panel, values=["All", "On-Time", "Delayed", "Boarding", "Scheduled", "Cancelled"], state="readonly", width=12, style="TCombobox")
        self.status_filter_cb.set("All")
        self.status_filter_cb.pack(side=tk.LEFT, padx=(0, 15))
        self.status_filter_cb.bind("<<ComboboxSelected>>", lambda e: self.refresh_data())

        ttk.Button(control_panel, text="Apply Filter", style="Cyan.TButton", command=self.refresh_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_panel, text="Reset", style="TButton", command=self._reset_filters).pack(side=tk.LEFT, padx=5)

        ttk.Button(control_panel, text="+ Add New Flight", style="Success.TButton", command=self._open_add_dialog).pack(side=tk.RIGHT, padx=5)

        # Table Container
        table_frame = ttk.Frame(self, style="Panel.TFrame", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ("flight_number", "airline_company", "departure_airport", "arrival_airport", "passenger_number", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("flight_number", text="Flight No")
        self.tree.heading("airline_company", text="Airline Company")
        self.tree.heading("departure_airport", text="Origin (Departure)")
        self.tree.heading("arrival_airport", text="Destination (Arrival)")
        self.tree.heading("passenger_number", text="Passengers")
        self.tree.heading("status", text="Operational Status")

        self.tree.column("flight_number", width=100, anchor="center")
        self.tree.column("airline_company", width=160, anchor="w")
        self.tree.column("departure_airport", width=120, anchor="center")
        self.tree.column("arrival_airport", width=120, anchor="center")
        self.tree.column("passenger_number", width=100, anchor="center")
        self.tree.column("status", width=130, anchor="center")

        # Color Tags
        self.tree.tag_configure("On-Time", foreground="#10b981")
        self.tree.tag_configure("Delayed", foreground="#f59e0b")
        self.tree.tag_configure("Boarding", foreground="#06b6d4")
        self.tree.tag_configure("Scheduled", foreground="#a855f7")
        self.tree.tag_configure("Cancelled", foreground="#ef4444")

        # Scrollbars
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)

        # Bottom Actions Bar
        action_bar = ttk.Frame(self, style="Panel.TFrame", padding=10)
        action_bar.pack(fill=tk.X, padx=10, pady=(5, 10))

        ttk.Label(action_bar, text="Quick Status Update for Selected Flight:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(action_bar, text="Mark On-Time", style="Success.TButton", command=lambda: self._quick_update_status("On-Time")).pack(side=tk.LEFT, padx=3)
        ttk.Button(action_bar, text="Mark Delayed", style="Warning.TButton", command=lambda: self._quick_update_status("Delayed")).pack(side=tk.LEFT, padx=3)
        ttk.Button(action_bar, text="Mark Boarding", style="Cyan.TButton", command=lambda: self._quick_update_status("Boarding")).pack(side=tk.LEFT, padx=3)
        ttk.Button(action_bar, text="Mark Cancelled", style="Danger.TButton", command=lambda: self._quick_update_status("Cancelled")).pack(side=tk.LEFT, padx=3)

        ttk.Button(action_bar, text="Delete Flight", style="Danger.TButton", command=self._delete_selected).pack(side=tk.RIGHT, padx=5)
        ttk.Button(action_bar, text="Refresh", style="TButton", command=self.refresh_data).pack(side=tk.RIGHT, padx=5)

        self.count_label = ttk.Label(action_bar, text="Total Flights: 0", style="Secondary.TLabel")
        self.count_label.pack(side=tk.RIGHT, padx=15)

    def refresh_data(self):
        search = self.search_var.get().strip() or None
        status = self.status_filter_cb.get().strip()
        try:
            rows, _ = queries.get_all_flights(search_term=search, status_filter=status)
            for item in self.tree.get_children():
                self.tree.delete(item)

            for r in rows:
                flight_num, airline, dep, arr, pax, st = r
                st_clean = st.strip()
                tag = st_clean if st_clean in ("On-Time", "Delayed", "Boarding", "Scheduled", "Cancelled") else ""
                self.tree.insert("", tk.END, values=(flight_num, airline, dep, arr, pax, st_clean), tags=(tag,))

            self.count_label.config(text=f"Total Flights: {len(rows)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load flight data:\n{e}", parent=self)

    def _reset_filters(self):
        self.search_var.set("")
        self.status_filter_cb.set("All")
        self.refresh_data()

    def _open_add_dialog(self):
        AddFlightDialog(self, on_save_callback=self.refresh_data)

    def _get_selected_flight(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selection Required", "Please select a flight row first.", parent=self)
            return None
        return self.tree.item(selected[0])["values"][0]

    def _quick_update_status(self, new_status: str):
        flight_num = self._get_selected_flight()
        if not flight_num:
            return
        try:
            queries.update_flight_status(flight_num, new_status)
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Update Error", f"Failed to update status for {flight_num}:\n{e}", parent=self)

    def _delete_selected(self):
        flight_num = self._get_selected_flight()
        if not flight_num:
            return
        if messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete flight {flight_num}?", parent=self):
            try:
                queries.delete_flight(flight_num)
                self.refresh_data()
            except Exception as e:
                messagebox.showerror("Delete Error", f"Failed to delete flight {flight_num}:\n{e}", parent=self)
