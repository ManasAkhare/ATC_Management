"""
Fleet Management & Horizontal Fragmentation View (ADBMS Concept 1).
Demonstrates horizontal partitioning into plane_commercial and plane_private
and reconstruction using UNION ALL.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system import queries
from atc_system.ui.theme import *

class AircraftView(ttk.Frame):
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
        ttk.Label(title_row, text="ADBMS Concept: Horizontal Fragmentation & Reconstruction", font=FONT_SUBTITLE, style="Subtitle.TLabel").pack(side=tk.LEFT)
        ttk.Button(title_row, text="Re-execute Fragmentation on DB", style="Cyan.TButton", command=self._rebuild_fragments).pack(side=tk.RIGHT)

        desc = (
            "Horizontal Fragmentation partitions a relation into disjoint subsets of tuples using selection predicates:\n"
            "• Fragment 1 (plane_commercial): SELECT * FROM aircraft WHERE Flight_Type = 'Commercial';\n"
            "• Fragment 2 (plane_private): SELECT * FROM aircraft WHERE Flight_Type = 'Private';\n"
            "• Reconstruction Rule: The global relation is reconstructed losslessly via UNION ALL."
        )
        ttk.Label(info_panel, text=desc, style="Secondary.TLabel", justify="left").pack(anchor="w", pady=(5, 0))

        # Notebook for Tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: Global Relation (Aircraft)
        self.tab_base = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_base, text="Base Relation (aircraft)")
        self.tree_base = self._create_tree(self.tab_base, ("plane_number", "plane_type", "manufacturer", "flight_type"), 
                                           ("Plane Number (PK)", "Model / Type", "Manufacturer", "Flight Classification"))

        # Tab 2: Commercial Fragment
        self.tab_comm = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_comm, text="Fragment 1: Commercial (plane_commercial)")
        self.tree_comm = self._create_tree(self.tab_comm, ("plane_number", "plane_type", "manufacturer", "flight_type"),
                                           ("Plane Number", "Model / Type", "Manufacturer", "Flight Classification"))

        # Tab 3: Private Fragment
        self.tab_priv = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_priv, text="Fragment 2: Private (plane_private)")
        self.tree_priv = self._create_tree(self.tab_priv, ("plane_number", "plane_type", "manufacturer", "flight_type"),
                                           ("Plane Number", "Model / Type", "Manufacturer", "Flight Classification"))

        # Tab 4: Reconstruction (UNION ALL)
        self.tab_recon = ttk.Frame(self.notebook, style="Panel.TFrame")
        self.notebook.add(self.tab_recon, text="Lossless Reconstruction (UNION ALL)")
        self.tree_recon = self._create_tree(self.tab_recon, ("plane_number", "plane_type", "manufacturer", "flight_type", "source_fragment"),
                                            ("Plane Number", "Model / Type", "Manufacturer", "Flight Classification", "Source Fragment"))

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
            # Base
            rows_base, _ = queries.get_aircraft_all()
            self._populate_tree(self.tree_base, rows_base)

            # Commercial
            rows_comm, _ = queries.get_aircraft_commercial()
            self._populate_tree(self.tree_comm, rows_comm)

            # Private
            rows_priv, _ = queries.get_aircraft_private()
            self._populate_tree(self.tree_priv, rows_priv)

            # Reconstructed
            rows_recon, _ = queries.get_reconstructed_horizontal()
            self._populate_tree(self.tree_recon, rows_recon)

            self.status_lbl.config(
                text=f"Base: {len(rows_base)} planes | Commercial Fragment: {len(rows_comm)} planes | Private Fragment: {len(rows_priv)} planes | Reconstructed: {len(rows_recon)}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load aircraft fragmentation data:\n{e}", parent=self)

    def _populate_tree(self, tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for r in rows:
            tree.insert("", tk.END, values=r)

    def _rebuild_fragments(self):
        try:
            success, msg = queries.rebuild_horizontal_fragments()
            messagebox.showinfo("Success", msg, parent=self)
            self.load_all_tabs()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rebuild fragments:\n{e}", parent=self)
