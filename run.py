"""
Air Traffic Control (ATC) Management System
Entry point to launch the offline desktop GUI application.
"""

import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from atc_system.ui.app import ATCManagementApp

def main():
    app = ATCManagementApp()
    app.mainloop()

if __name__ == "__main__":
    main()
