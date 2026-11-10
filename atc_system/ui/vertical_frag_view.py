"""
Vertical Fragmentation & Lossless Join Decomposition View (ADBMS Concept 2).
Demonstrates vertical partitioning of flight into plane_info and route_info,
and reassembly via Natural / Inner Join on Flight_Number.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system import queries
from atc_system.ui.theme import *

class VerticalFragView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()
        self.load_all_tabs()

    def _build_ui(self):
        # Header Concept Explanation Box
        info_panel = ttk.Frame(self, style="Panel.TFrame", padding=12)
        info_panel.pack(fill=tk.X, padx=10, pady=(10, 5))

        title_row = ttk.Frame(info_panel, style="Panel.TFrame")
        title_row.pack(fill=tk.X)
        ttk.Label(title_row, text="ADBMS Concept: Vertical Fragmentation & Lossless Join Reassembly", font=FONT_SUBTITLE, style="Subtitle.TLabel").pack(side=tk.LEFT)
        ttk.Button(title_row, text="Re-execute Vertical Fragmentation on DB", style="Cyan.TButton", command=self._rebuild_fragments).pack(side=tk.RIGHT)

        desc = (
            "Vertical Fragmentation splits a relation into subsets of attributes (columns) containing the primary key:\n"
            "• Fragment 1 (plane_info): SELECT Flight_Number, Airline_Company, Passenger_Number FROM flight;\n"
            "• Fragment 2 (route_info): SELECT Flight_Number, Departure_Airport, Arrival_Airport, Status FROM flight;\n"
            "• Lossless Join Rule: Reassembled without loss or spurious tuples using: plane_info ⨝ route_info ON Flight_Number."
        )
        ttk.Label(info_panel, text=desc, style="Secondary.TLabel", justify="left").pack(anchor="w", pady=(5, 0))

        # Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: Fragment 1 (plane_info)
        self.tab_plane = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_plane, text="Fragment 1: Aircraft / Capacity (plane_info)")
        self.tree_plane = self._create_tree(self.tab_plane, ("flight_number", "airline_company", "passenger_number"),
                                            ("Flight Number (PK)", "Airline Operator", "Passenger Capacity"))

        # Tab 2: Fragment 2 (route_info)
        self.tab_route = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_route, text="Fragment 2: Route & Status (route_info)")
        self.tree_route = self._create_tree(self.tab_route, ("flight_number", "departure_airport", "arrival_airport", "status"),
                                            ("Flight Number (PK)", "Origin Airport", "Destination Airport", "Flight Status"))

        # Tab 3: Reconstructed Relation (Natural Join)
        self.tab_recon = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_recon, text="Reconstructed Relation (plane_info ⨝ route_info)")
        self.tree_recon = self._create_tree(self.tab_recon, 
                                            ("flight_number", "airline_company", "passenger_number", "departure_airport", "arrival_airport", "status"),
                                            ("Flight Number", "Airline", "Passengers", "Origin", "Destination", "Status"))

        # Bottom Bar
        bottom_bar = ttk.Frame(self, style="Panel.TFrame", padding=8)
        bottom_bar.pack(fill=tk.X, padx=10, pady=(5, 10))
        self.status_lbl = ttk.Label(bottom_bar, text="Ready", style="Secondary.TLabel")
        self.status_lbl.pack(side=tk.LEFT)
        ttk.Button(bottom_bar, text="Refresh All", style="TButton", command=self.load_all_tabs).pack(side=tk.RIGHT)

    def _create_tree(self, parent, columns, headings):
        frame = ttk.Frame(parent, style="Panel.TFrame", padding=10)
        frame.pack(fill=tk.BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col, heading in zip(columns, headings):
            tree.heading(col, text=heading)
            tree.column(col, anchor="w", width=140)

        vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        return tree

    def load_all_tabs(self):
        try:
            # plane_info
            rows_plane, _ = queries.get_plane_info()
            self._populate_tree(self.tree_plane, rows_plane)

            # route_info
            rows_route, _ = queries.get_route_info()
            self._populate_tree(self.tree_route, rows_route)

            # Reconstructed Join
            rows_recon, _ = queries.get_reconstructed_vertical()
            self._populate_tree(self.tree_recon, rows_recon)

            self.status_lbl.config(
                text=f"plane_info: {len(rows_plane)} rows | route_info: {len(rows_route)} rows | Lossless Join: {len(rows_recon)} reassembled flights."
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load vertical fragmentation data:\n{e}", parent=self)

    def _populate_tree(self, tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for r in rows:
            tree.insert("", tk.END, values=r)

    def _rebuild_fragments(self):
        try:
            success, msg = queries.rebuild_vertical_fragments()
            messagebox.showinfo("Success", msg, parent=self)
            self.load_all_tabs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rebuild fragments:\n{e}", parent=self)
