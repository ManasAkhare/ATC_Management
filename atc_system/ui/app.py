"""
Main Application Window for ATC Management System.
Aviation Command Center GUI with sidebar navigation, top status bar, and modular views.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system.db import db_manager
from atc_system.config import Config
from atc_system.ui.theme import *
from atc_system.ui.connection_dialog import ConnectionDialog
from atc_system.ui.flights_view import FlightsView
from atc_system.ui.aircraft_view import AircraftView
from atc_system.ui.vertical_frag_view import VerticalFragView
from atc_system.ui.schedule_view import ScheduleView
from atc_system.ui.crew_view import CrewView
from atc_system.ui.xml_data_view import XmlDataView
from atc_system.ui.security_view import SecurityView
from atc_system.ui.analytics_view import AnalyticsView
from atc_system.ui.query_console import QueryConsoleView

class ATCManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Air Traffic Control (ATC) Management System - ADBMS")
        self.geometry("1240x780")
        self.minsize(1050, 680)

        apply_theme(self)

        self._build_header()
        self._build_main_layout()
        self._build_statusbar()

        # Connect to DB
        self._init_connection()

        # Select initial view
        self._switch_view("flights")

    def _init_connection(self):
        success, msg = db_manager.connect()
        self._update_connection_status(success)
        if not success:
            messagebox.showwarning(
                "Database Connection",
                f"Could not connect to PostgreSQL ({Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}):\n\n{msg}\n\n"
                "Please configure your connection credentials via 'Connection Settings'.",
                parent=self
            )

    def _build_header(self):
        header = ttk.Frame(self, style="Header.TFrame", padding=(15, 10))
        header.pack(fill=tk.X, side=tk.TOP)

        # Title and Subtitle
        title_box = ttk.Frame(header, style="Header.TFrame")
        title_box.pack(side=tk.LEFT)

        ttk.Label(title_box, text="✈ AIR TRAFFIC CONTROL MANAGEMENT SYSTEM", font=FONT_TITLE, foreground="#38bdf8", style="Header.TFrame").pack(anchor="w")
        ttk.Label(title_box, text="Advanced Database Management Systems (ADBMS) Project", font=FONT_BODY, foreground=TEXT_SECONDARY, style="Header.TFrame").pack(anchor="w")

        # Right status badges and actions
        actions_box = ttk.Frame(header, style="Header.TFrame")
        actions_box.pack(side=tk.RIGHT)

        self.conn_badge = ttk.Label(
            actions_box,
            text="● CONNECTING...",
            font=FONT_BADGE,
            foreground="#f59e0b",
            background="#1e293b",
            padding=(10, 5)
        )
        self.conn_badge.pack(side=tk.LEFT, padx=6)

        self.role_badge = ttk.Label(
            actions_box,
            text="USER: postgres",
            font=FONT_BADGE,
            foreground="#38bdf8",
            background="#1e293b",
            padding=(10, 5)
        )
        self.role_badge.pack(side=tk.LEFT, padx=6)

        ttk.Button(actions_box, text="⚙ Connection Settings", style="Cyan.TButton", command=self._open_connection_dialog).pack(side=tk.LEFT, padx=6)

    def _build_main_layout(self):
        body = ttk.Frame(self, style="TFrame")
        body.pack(fill=tk.BOTH, expand=True, side=tk.TOP)

        # Left Sidebar Navigation
        sidebar = ttk.Frame(body, style="Sidebar.TFrame", width=230, padding=10)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        ttk.Label(sidebar, text="SYSTEM MODULES", font=FONT_BADGE, foreground=TEXT_MUTED, background=SIDEBAR_BG).pack(anchor="w", pady=(5, 10), padx=5)

        self.nav_buttons = {}
        nav_items = [
            ("flights", "✈ Live Flights Monitor"),
            ("aircraft", "🏢 Horizontal Fragmentation"),
            ("vertical", "🔀 Vertical Fragmentation"),
            ("schedule", "🛫 Runway & Conflict Radar"),
            ("crew", "👨‍✈️ Flight Crew & Pilots"),
            ("xml_data", "📄 XML & XPath Engine"),
            ("security", "🛡 Security & RLS Policy"),
            ("analytics", "📊 Operations Analytics"),
            ("console", "💻 SQL Query Console"),
        ]

        for view_key, label_text in nav_items:
            btn = tk.Button(
                sidebar,
                text=label_text,
                font=FONT_BODY_BOLD,
                bg="#131f37",
                fg=TEXT_PRIMARY,
                activebackground=ACCENT_BLUE,
                activeforeground="#ffffff",
                relief="flat",
                anchor="w",
                padx=12,
                pady=9,
                cursor="hand2",
                command=lambda k=view_key: self._switch_view(k)
            )
            btn.pack(fill=tk.X, pady=2)
            self.nav_buttons[view_key] = btn

        # Content View Container
        self.container = ttk.Frame(body, style="TFrame")
        self.container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.views = {}

    def _build_statusbar(self):
        statusbar = ttk.Frame(self, style="Header.TFrame", padding=(12, 4))
        statusbar.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_left = ttk.Label(statusbar, text="Ready", font=FONT_BODY, foreground=TEXT_SECONDARY, style="Header.TFrame")
        self.status_left.pack(side=tk.LEFT)

        self.status_right = ttk.Label(statusbar, text=f"Target Database: {Config.DB_NAME} | Mode: Offline Desktop", font=FONT_BODY, foreground=TEXT_MUTED, style="Header.TFrame")
        self.status_right.pack(side=tk.RIGHT)

    def _switch_view(self, view_key: str):
        # Update button highlights
        for key, btn in self.nav_buttons.items():
            if key == view_key:
                btn.configure(bg=ACCENT_BLUE, fg="#ffffff")
            else:
                btn.configure(bg="#131f37", fg=TEXT_PRIMARY)

        # Lazy load or raise view
        if view_key not in self.views:
            if view_key == "flights":
                self.views[view_key] = FlightsView(self.container)
            elif view_key == "aircraft":
                self.views[view_key] = AircraftView(self.container)
            elif view_key == "vertical":
                self.views[view_key] = VerticalFragView(self.container)
            elif view_key == "schedule":
                self.views[view_key] = ScheduleView(self.container)
            elif view_key == "crew":
                self.views[view_key] = CrewView(self.container)
            elif view_key == "xml_data":
                self.views[view_key] = XmlDataView(self.container)
            elif view_key == "security":
                self.views[view_key] = SecurityView(self.container, on_role_changed_callback=self._on_role_changed)
            elif view_key == "analytics":
                self.views[view_key] = AnalyticsView(self.container)
            elif view_key == "console":
                self.views[view_key] = QueryConsoleView(self.container)

        for v in self.views.values():
            v.pack_forget()

        self.views[view_key].pack(fill=tk.BOTH, expand=True)
        self.status_left.config(text=f"Active Module: {view_key.replace('_', ' ').title()}")

    def _update_connection_status(self, is_connected: bool):
        if is_connected:
            self.conn_badge.config(text=f"● CONNECTED ({Config.DB_NAME})", foreground="#10b981")
            role = db_manager.get_current_role()
            self.role_badge.config(text=f"USER: {role.upper()}")
        else:
            self.conn_badge.config(text="● DISCONNECTED", foreground="#ef4444")

    def _on_role_changed(self, new_role: str):
        self.role_badge.config(text=f"USER: {new_role.upper()}")
        self.status_left.config(text=f"Switched session role to '{new_role}'. Row-Level Security active.")
        # If flights view is active, refresh it to show RLS effect
        if "flights" in self.views:
            self.views["flights"].refresh_data()

    def _open_connection_dialog(self):
        ConnectionDialog(self, on_reconnect_callback=self._on_reconnected)

    def _on_reconnected(self):
        self._update_connection_status(db_manager.is_connected())
        # Reload views
        for v in self.views.values():
            if hasattr(v, "refresh_data"):
                v.refresh_data()
            elif hasattr(v, "load_all_tabs"):
                v.load_all_tabs()
            elif hasattr(v, "refresh_all"):
                v.refresh_all()
