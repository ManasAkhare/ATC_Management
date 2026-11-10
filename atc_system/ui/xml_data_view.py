"""
Semi-Structured Data & XML Database Engine View (ADBMS Concept 4).
Demonstrates XML storage, native XPath querying, and XMLTABLE relational shredding.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import xml.dom.minidom
from atc_system import queries
from atc_system.ui.theme import *

class XmlDataView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()
        self.load_xml_catalog()
        self.load_xmltable()

    def _build_ui(self):
        # Header Box
        info_panel = ttk.Frame(self, style="Panel.TFrame", padding=12)
        info_panel.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(info_panel, text="ADBMS Concept: Native XML Database & XPath Query Processing", font=FONT_SUBTITLE, style="Subtitle.TLabel").pack(anchor="w")
        desc = (
            "PostgreSQL natively supports semi-structured XML data with XPath query evaluation and XMLTABLE shredding:\n"
            "• xpath(path, xml_data): Evaluates XPath 1.0 expressions against XML documents returning matched node arrays.\n"
            "• XMLTABLE: Shreds hierarchical XML documents into standard SQL relational rows and columns."
        )
        ttk.Label(info_panel, text=desc, style="Secondary.TLabel", justify="left").pack(anchor="w", pady=(4, 0))

        # Notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: XML Catalog Viewer
        self.tab_doc = ttk.Frame(self.notebook, style="Panel.TFrame", padding=10)
        self.notebook.add(self.tab_doc, text="1. Stored XML Document (FlightCatalog)")

        doc_top = ttk.Frame(self.tab_doc, style="Panel.TFrame")
        doc_top.pack(fill=tk.X, pady=(0, 5))
        ttk.Label(doc_top, text="Raw XML Document in Flight_Data (xml_content XML):", font=FONT_HEADING, style="Panel.TLabel").pack(side=tk.LEFT)
        ttk.Button(doc_top, text="Reload XML", style="TButton", command=self.load_xml_catalog).pack(side=tk.RIGHT)

        self.txt_xml = tk.Text(
            self.tab_doc,
            bg="#111c33",
            fg="#38bdf8",
            insertbackground="#ffffff",
            font=FONT_MONO,
            wrap="none",
            borderwidth=0,
            padx=10,
            pady=10
        )
        sb_xml_y = ttk.Scrollbar(self.tab_doc, orient="vertical", command=self.txt_xml.yview)
        sb_xml_x = ttk.Scrollbar(self.tab_doc, orient="horizontal", command=self.txt_xml.xview)
        self.txt_xml.configure(yscrollcommand=sb_xml_y.set, xscrollcommand=sb_xml_x.set)

        self.txt_xml.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb_xml_y.pack(side=tk.RIGHT, fill=tk.Y)
        sb_xml_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Tab 2: XPath Query Terminal
        self.tab_xpath = ttk.Frame(self.notebook, style="Panel.TFrame", padding=10)
        self.notebook.add(self.tab_xpath, text="2. Native XPath Query Engine")

        query_box = ttk.Frame(self.tab_xpath, style="Panel.TFrame")
        query_box.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(query_box, text="Preset XPath Queries:", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(anchor="w")
        preset_row = ttk.Frame(query_box, style="Panel.TFrame")
        preset_row.pack(fill=tk.X, pady=(3, 8))

        presets = [
            ("IndiGo Flights", '//Flight[Airline="IndiGo"]'),
            ("Departing BOM", '//Flight[Departure="BOM"]'),
            ("Delayed Flights", '//Flight[Status="Delayed"]'),
            ("Arriving BLR", '//Flight[Arrival="BLR"]'),
            ("IndiGo Flight Numbers", '//Flight[Airline="IndiGo"]/FlightNumber/text()'),
        ]

        for name, expr in presets:
            ttk.Button(preset_row, text=name, style="Cyan.TButton", command=lambda e=expr: self._set_xpath(e)).pack(side=tk.LEFT, padx=3)

        ttk.Label(query_box, text="XPath Expression (evaluated on PostgreSQL server):", style="Panel.TLabel", font=FONT_BODY_BOLD).pack(anchor="w", pady=(5, 2))
        expr_row = ttk.Frame(query_box, style="Panel.TFrame")
        expr_row.pack(fill=tk.X)

        self.xpath_entry = ttk.Entry(expr_row, style="TEntry", font=FONT_MONO)
        self.xpath_entry.insert(0, '//Flight[Airline="IndiGo"]')
        self.xpath_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.xpath_entry.bind("<Return>", lambda e: self.execute_xpath())

        ttk.Button(expr_row, text="Execute XPath", style="Success.TButton", command=self.execute_xpath).pack(side=tk.RIGHT)

        # Results area for XPath
        ttk.Label(self.tab_xpath, text="Matched XPath Node Results:", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(10, 4))
        self.txt_xpath_result = tk.Text(
            self.tab_xpath,
            bg="#111c33",
            fg="#4ade80",
            insertbackground="#ffffff",
            font=FONT_MONO,
            wrap="word",
            borderwidth=0,
            padx=10,
            pady=10
        )
        self.txt_xpath_result.pack(fill=tk.BOTH, expand=True)

        # Tab 3: XMLTABLE Shredding
        self.tab_shred = ttk.Frame(self.notebook, style="Panel.TFrame", padding=10)
        self.notebook.add(self.tab_shred, text="3. XMLTABLE Relational Shredder")

        shred_top = ttk.Frame(self.tab_shred, style="Panel.TFrame")
        shred_top.pack(fill=tk.X, pady=(0, 8))
        ttk.Label(shred_top, text="Transformed Relational View via PostgreSQL XMLTABLE:", font=FONT_HEADING, style="Panel.TLabel").pack(side=tk.LEFT)
        ttk.Button(shred_top, text="Re-execute XMLTABLE", style="Cyan.TButton", command=self.load_xmltable).pack(side=tk.RIGHT)

        shred_cols = ("flight_no", "airline", "from_city", "to_city", "status")
        self.tree_shred = ttk.Treeview(self.tab_shred, columns=shred_cols, show="headings")
        self.tree_shred.heading("flight_no", text="Flight No (XPath: FlightNumber)")
        self.tree_shred.heading("airline", text="Airline (XPath: Airline)")
        self.tree_shred.heading("from_city", text="Origin (XPath: Departure)")
        self.tree_shred.heading("to_city", text="Destination (XPath: Arrival)")
        self.tree_shred.heading("status", text="Status (XPath: Status)")

        for c in shred_cols:
            self.tree_shred.column(c, anchor="center", width=140)

        vsb_s = ttk.Scrollbar(self.tab_shred, orient="vertical", command=self.tree_shred.yview)
        self.tree_shred.configure(yscrollcommand=vsb_s.set)
        self.tree_shred.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb_s.pack(side=tk.RIGHT, fill=tk.Y)

    def load_xml_catalog(self):
        try:
            rows, _ = queries.get_raw_xml_documents()
            self.txt_xml.delete("1.0", tk.END)
            if rows:
                doc_id, raw_xml = rows[0]
                try:
                    dom = xml.dom.minidom.parseString(raw_xml)
                    pretty = dom.toprettyxml(indent="    ")
                    # remove excess blank lines
                    lines = [l for l in pretty.splitlines() if l.strip()]
                    self.txt_xml.insert("1.0", "\n".join(lines))
                except Exception:
                    self.txt_xml.insert("1.0", raw_xml)
            else:
                self.txt_xml.insert("1.0", "No XML document found in table Flight_Data.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load XML catalog:\n{e}", parent=self)

    def _set_xpath(self, expr: str):
        self.xpath_entry.delete(0, tk.END)
        self.xpath_entry.insert(0, expr)
        self.execute_xpath()

    def execute_xpath(self):
        expr = self.xpath_entry.get().strip()
        if not expr:
            messagebox.showwarning("Validation", "Please enter an XPath expression.", parent=self)
            return

        try:
            rows, _ = queries.execute_xpath_query(expr)
            self.txt_xpath_result.delete("1.0", tk.END)
            if not rows or not rows[0][1]:
                self.txt_xpath_result.insert("1.0", f"-- Query: xpath('{expr}', xml_content)\n-- Result: 0 nodes matched.\n")
                return

            matched = rows[0][1]
            header = f"-- PostgreSQL Function: xpath('{expr}', xml_content)\n-- Total Nodes Matched: {len(matched)}\n" + ("=" * 60) + "\n\n"
            self.txt_xpath_result.insert("1.0", header)

            for i, node in enumerate(matched, start=1):
                clean_node = node.strip()
                try:
                    dom = xml.dom.minidom.parseString(f"<root>{clean_node}</root>")
                    pretty = dom.toprettyxml(indent="    ")
                    lines = [l for l in pretty.splitlines() if l.strip() and "<root>" not in l and "</root>" not in l and "<?" not in l]
                    formatted = "\n".join(lines)
                except Exception:
                    formatted = clean_node

                self.txt_xpath_result.insert(tk.END, f"[Match #{i}]\n{formatted}\n\n")

        except Exception as e:
            messagebox.showerror("XPath Error", f"Failed to execute XPath query:\n{e}", parent=self)

    def load_xmltable(self):
        try:
            rows, _ = queries.get_xmltable_shredded()
            for item in self.tree_shred.get_children():
                self.tree_shred.delete(item)
            for r in rows:
                self.tree_shred.insert("", tk.END, values=r)
        except Exception as e:
            messagebox.showerror("XMLTABLE Error", f"Failed to load XMLTABLE shredded data:\n{e}", parent=self)
