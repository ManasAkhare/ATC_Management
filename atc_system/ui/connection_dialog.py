"""
Connection Settings Dialog for ATC Management System.
Allows testing and updating PostgreSQL credentials dynamically.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from atc_system.config import Config
from atc_system.db import db_manager
from atc_system.ui.theme import *

class ConnectionDialog(tk.Toplevel):
    def __init__(self, parent, on_reconnect_callback=None):
        super().__init__(parent)
        self.title("PostgreSQL Database Connection Settings")
        self.geometry("450x360")
        self.resizable(False, False)
        self.configure(bg=BG_DARK)
        self.transient(parent)
        self.grab_set()

        self.on_reconnect_callback = on_reconnect_callback

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
        container = ttk.Frame(self, style="Panel.TFrame", padding=20)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        ttk.Label(container, text="Database Connection Parameters", font=FONT_SUBTITLE, style="Subtitle.TLabel").pack(anchor="w", pady=(0, 15))

        fields = [
            ("Host:", "host", Config.DB_HOST),
            ("Port:", "port", str(Config.DB_PORT)),
            ("Database:", "dbname", Config.DB_NAME),
            ("Username:", "user", Config.DB_USER),
            ("Password:", "password", Config.DB_PASSWORD),
        ]

        self.entries = {}
        for label_text, key, default_val in fields:
            row = ttk.Frame(container, style="Panel.TFrame")
            row.pack(fill=tk.X, pady=4)
            ttk.Label(row, text=label_text, width=12, style="Panel.TLabel", font=FONT_BODY_BOLD).pack(side=tk.LEFT)
            entry = ttk.Entry(row, style="TEntry", show="*" if key == "password" else "")
            entry.insert(0, default_val)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            self.entries[key] = entry

        btn_row = ttk.Frame(container, style="Panel.TFrame")
        btn_row.pack(fill=tk.X, pady=(20, 0))

        ttk.Button(btn_row, text="Test Connection", style="Cyan.TButton", command=self._test_connection).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row, text="Save & Connect", style="TButton", command=self._save_and_connect).pack(side=tk.RIGHT)

    def _test_connection(self):
        host = self.entries["host"].get().strip()
        port = int(self.entries["port"].get().strip())
        dbname = self.entries["dbname"].get().strip()
        user = self.entries["user"].get().strip()
        password = self.entries["password"].get()

        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password,
                connect_timeout=3
            )
            conn.close()
            messagebox.showinfo("Success", f"Successfully connected to database '{dbname}' on {host}:{port}!", parent=self)
        except Exception as e:
            messagebox.showerror("Connection Failed", f"Could not connect to PostgreSQL:\n\n{e}", parent=self)

    def _save_and_connect(self):
        host = self.entries["host"].get().strip()
        port = int(self.entries["port"].get().strip())
        dbname = self.entries["dbname"].get().strip()
        user = self.entries["user"].get().strip()
        password = self.entries["password"].get()

        Config.update_connection(host, port, dbname, user, password)
        db_manager.close()
        success, msg = db_manager.connect()

        if success:
            messagebox.showinfo("Connected", "Settings saved and connected successfully!", parent=self)
            if self.on_reconnect_callback:
                self.on_reconnect_callback()
            self.destroy()
        else:
            messagebox.showwarning("Warning", f"Saved configuration, but connection failed:\n{msg}", parent=self)
            self.destroy()
