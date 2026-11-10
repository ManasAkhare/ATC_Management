"""
Analytics and Visual ATC Operations Dashboard.
Visualizes flight status distributions, airline shares, and runway utilization
using native offline Tkinter graphics.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from atc_system import queries
from atc_system.ui.theme import *

class AnalyticsView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, style="TFrame")
        self._build_ui()
        self.refresh_data()

    def _build_ui(self):
        # Top KPI Cards Panel
        self.kpi_frame = ttk.Frame(self, style="TFrame")
        self.kpi_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        self.card_flights = self._create_kpi_card(self.kpi_frame, "Total Flights", "0", ACCENT_CYAN)
        self.card_passengers = self._create_kpi_card(self.kpi_frame, "Total Passengers", "0", ACCENT_BLUE)
        self.card_ontime = self._create_kpi_card(self.kpi_frame, "On-Time Rate", "0%", ACCENT_GREEN)
        self.card_delayed = self._create_kpi_card(self.kpi_frame, "Delayed Flights", "0", ACCENT_AMBER)

        # Charts Area (2 horizontal charts side by side, and 1 bottom chart)
        charts_container = ttk.Frame(self, style="TFrame")
        charts_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left Chart: Status Breakdown
        chart_left = ttk.Frame(charts_container, style="Panel.TFrame", padding=10)
        chart_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        ttk.Label(chart_left, text="Flights by Operational Status", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 6))

        self.canvas_status = tk.Canvas(chart_left, bg="#111c33", highlightthickness=0, height=220)
        self.canvas_status.pack(fill=tk.BOTH, expand=True)

        # Right Chart: Airline Volume
        chart_right = ttk.Frame(charts_container, style="Panel.TFrame", padding=10)
        chart_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        ttk.Label(chart_right, text="Flights by Airline Operator", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 6))

        self.canvas_airline = tk.Canvas(chart_right, bg="#111c33", highlightthickness=0, height=220)
        self.canvas_airline.pack(fill=tk.BOTH, expand=True)

        # Bottom Chart: Runway Utilization
        chart_bottom = ttk.Frame(self, style="Panel.TFrame", padding=10)
        chart_bottom.pack(fill=tk.X, padx=10, pady=(5, 10))
        ttk.Label(chart_bottom, text="Runway Slot Utilization (Scheduled Movements)", font=FONT_HEADING, style="Panel.TLabel").pack(anchor="w", pady=(0, 6))

        self.canvas_runway = tk.Canvas(chart_bottom, bg="#111c33", highlightthickness=0, height=130)
        self.canvas_runway.pack(fill=tk.X, expand=True)

    def _create_kpi_card(self, parent, title: str, value: str, color: str):
        card = ttk.Frame(parent, style="Panel.TFrame", padding=12)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        ttk.Label(card, text=title.upper(), style="Secondary.TLabel", font=FONT_BADGE).pack(anchor="w")
        val_lbl = ttk.Label(card, text=value, font=(FONT_FAMILY, 18, "bold"), foreground=color, style="Panel.TLabel")
        val_lbl.pack(anchor="w", pady=(4, 0))
        return val_lbl

    def refresh_data(self):
        try:
            # 1. Passenger Stats
            pstats = queries.get_passenger_statistics()
            total_flights = pstats.get("total_flights", 0)
            total_pax = pstats.get("total_passengers", 0)
            self.card_flights.config(text=f"{total_flights:,}")
            self.card_passengers.config(text=f"{total_pax:,}")

            # 2. Status counts
            status_rows = queries.get_flight_status_counts()
            ontime_count = 0
            delayed_count = 0
            for st, cnt in status_rows:
                if st == "On-Time":
                    ontime_count = cnt
                elif st == "Delayed":
                    delayed_count = cnt

            ontime_rate = round((ontime_count / total_flights * 100), 1) if total_flights else 0
            self.card_ontime.config(text=f"{ontime_rate}%")
            self.card_delayed.config(text=f"{delayed_count}")

            self._draw_horizontal_bar_chart(self.canvas_status, status_rows, {
                "On-Time": "#10b981",
                "Delayed": "#f59e0b",
                "Boarding": "#06b6d4",
                "Scheduled": "#8b5cf6",
                "Cancelled": "#ef4444"
            })

            # 3. Airline volume
            airline_rows = queries.get_airline_distribution()
            self._draw_horizontal_bar_chart(self.canvas_airline, airline_rows[:6], default_color="#3b82f6")

            # 4. Runway utilization
            runway_rows = queries.get_runway_utilization()
            formatted_runways = [(f"Runway {r[0]}", r[1]) for r in runway_rows]
            self._draw_horizontal_bar_chart(self.canvas_runway, formatted_runways, default_color="#06b6d4")

        except Exception as e:
            messagebox.showerror("Analytics Error", f"Failed to compute operational analytics:\n{e}", parent=self)

    def _draw_horizontal_bar_chart(self, canvas: tk.Canvas, data, color_map=None, default_color="#3b82f6"):
        canvas.delete("all")
        canvas.update_idletasks()
        w = canvas.winfo_width()
        h = canvas.winfo_height()

        if w < 50 or h < 50 or not data:
            return

        max_val = max(v for _, v in data) if data else 1
        num_items = len(data)
        bar_height = min(24, int((h - 20) / max(num_items, 1) - 6))
        start_y = 10
        label_width = 120
        chart_width = w - label_width - 60

        for i, (label, val) in enumerate(data):
            y1 = start_y + i * (bar_height + 8)
            y2 = y1 + bar_height
            bar_len = int((val / max_val) * chart_width) if max_val else 0

            color = color_map.get(label, default_color) if color_map else default_color

            # Label
            canvas.create_text(
                label_width - 8, y1 + bar_height // 2,
                text=label,
                fill=TEXT_SECONDARY,
                font=FONT_BODY_BOLD,
                anchor="e"
            )

            # Bar
            canvas.create_rectangle(
                label_width, y1,
                label_width + bar_len, y2,
                fill=color,
                outline="",
            )

            # Value label
            canvas.create_text(
                label_width + bar_len + 8, y1 + bar_height // 2,
                text=str(val),
                fill=TEXT_PRIMARY,
                font=FONT_BODY_BOLD,
                anchor="w"
            )
