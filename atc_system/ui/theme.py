"""
Modern Aviation Dark/Light Theme and Styling for Tkinter/TTK.
"""

import tkinter as tk
from tkinter import ttk

# Aviation Command Center Palette
BG_DARK = "#0b1329"        # Deep midnight blue / black
PANEL_BG = "#131f37"       # Card / container background
SIDEBAR_BG = "#0d172e"     # Sidebar background
HEADER_BG = "#101a33"      # Header bar
TEXT_PRIMARY = "#f8fafc"   # High contrast crisp white
TEXT_SECONDARY = "#94a3b8" # Cool grey secondary text
TEXT_MUTED = "#64748b"     # Muted text

ACCENT_CYAN = "#06b6d4"    # Primary highlight / radar cyan
ACCENT_BLUE = "#3b82f6"    # Active tabs / primary actions
ACCENT_GREEN = "#10b981"   # On-time / success
ACCENT_AMBER = "#f59e0b"   # Delayed / warning
ACCENT_RED = "#ef4444"     # Conflict / critical hazard
ACCENT_PURPLE = "#8b5cf6"  # Scheduled / XML

BORDER_COLOR = "#22314e"
INPUT_BG = "#1c2b4a"

FONT_FAMILY = "Segoe UI"
FONT_TITLE = (FONT_FAMILY, 15, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 12, "bold")
FONT_HEADING = (FONT_FAMILY, 11, "bold")
FONT_BODY = (FONT_FAMILY, 9)
FONT_BODY_BOLD = (FONT_FAMILY, 9, "bold")
FONT_MONO = ("Consolas", 9)
FONT_BADGE = (FONT_FAMILY, 8, "bold")

def apply_theme(root: tk.Tk):
    """Applies modern custom TTK styling to the root window."""
    root.configure(bg=BG_DARK)
    style = ttk.Style(root)
    style.theme_use("clam")

    # Frames
    style.configure("TFrame", background=BG_DARK)
    style.configure("Panel.TFrame", background=PANEL_BG)
    style.configure("Sidebar.TFrame", background=SIDEBAR_BG)
    style.configure("Header.TFrame", background=HEADER_BG)

    # Labels
    style.configure("TLabel", background=BG_DARK, foreground=TEXT_PRIMARY, font=FONT_BODY)
    style.configure("Panel.TLabel", background=PANEL_BG, foreground=TEXT_PRIMARY, font=FONT_BODY)
    style.configure("Title.TLabel", background=HEADER_BG, foreground=TEXT_PRIMARY, font=FONT_TITLE)
    style.configure("Subtitle.TLabel", background=PANEL_BG, foreground=ACCENT_CYAN, font=FONT_SUBTITLE)
    style.configure("Secondary.TLabel", background=PANEL_BG, foreground=TEXT_SECONDARY, font=FONT_BODY)
    style.configure("Muted.TLabel", background=BG_DARK, foreground=TEXT_MUTED, font=FONT_BODY)

    # Buttons
    style.configure(
        "TButton",
        background=ACCENT_BLUE,
        foreground="#ffffff",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        focuscolor="none",
        padding=(10, 5)
    )
    style.map(
        "TButton",
        background=[("active", "#2563eb"), ("disabled", "#334155")],
        foreground=[("disabled", "#64748b")]
    )

    style.configure(
        "Cyan.TButton",
        background=ACCENT_CYAN,
        foreground="#000000",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(10, 5)
    )
    style.map("Cyan.TButton", background=[("active", "#0891b2")])

    style.configure(
        "Success.TButton",
        background=ACCENT_GREEN,
        foreground="#ffffff",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(8, 4)
    )
    style.map("Success.TButton", background=[("active", "#059669")])

    style.configure(
        "Warning.TButton",
        background=ACCENT_AMBER,
        foreground="#000000",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(8, 4)
    )
    style.map("Warning.TButton", background=[("active", "#d97706")])

    style.configure(
        "Danger.TButton",
        background=ACCENT_RED,
        foreground="#ffffff",
        font=FONT_BODY_BOLD,
        borderwidth=0,
        padding=(8, 4)
    )
    style.map("Danger.TButton", background=[("active", "#dc2626")])

    # Treeview (Data Tables)
    style.configure(
        "Treeview",
        background="#16223b",
        foreground=TEXT_PRIMARY,
        fieldbackground="#16223b",
        font=FONT_BODY,
        rowheight=26,
        borderwidth=0
    )
    style.configure(
        "Treeview.Heading",
        background="#1d2e50",
        foreground=ACCENT_CYAN,
        font=FONT_HEADING,
        borderwidth=1,
        relief="flat",
        padding=(6, 4)
    )
    style.map(
        "Treeview",
        background=[("selected", "#2563eb")],
        foreground=[("selected", "#ffffff")]
    )
    style.map("Treeview.Heading", background=[("active", "#2a4374")])

    # Notebook (Tab Controls)
    style.configure("TNotebook", background=BG_DARK, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        background="#18253f",
        foreground=TEXT_SECONDARY,
        font=FONT_BODY_BOLD,
        padding=(14, 7),
        borderwidth=0
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", ACCENT_BLUE)],
        foreground=[("selected", "#ffffff")]
    )

    # Entry and Combobox
    style.configure(
        "TEntry",
        fieldbackground=INPUT_BG,
        foreground=TEXT_PRIMARY,
        insertcolor=TEXT_PRIMARY,
        font=FONT_BODY,
        padding=4
    )
    style.configure(
        "TCombobox",
        fieldbackground=INPUT_BG,
        background=INPUT_BG,
        foreground=TEXT_PRIMARY,
        font=FONT_BODY,
        arrowcolor=ACCENT_CYAN,
        padding=4
    )
    style.map(
        "TCombobox",
        fieldbackground=[("readonly", INPUT_BG)],
        selectbackground=[("readonly", "#2563eb")],
        selectforeground=[("readonly", "#ffffff")]
    )

    # Scrollbar
    style.configure(
        "Vertical.TScrollbar",
        background=PANEL_BG,
        troughcolor=BG_DARK,
        arrowcolor=TEXT_SECONDARY,
        borderwidth=0
    )
    style.configure(
        "Horizontal.TScrollbar",
        background=PANEL_BG,
        troughcolor=BG_DARK,
        arrowcolor=TEXT_SECONDARY,
        borderwidth=0
    )
