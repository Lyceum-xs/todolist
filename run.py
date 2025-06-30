from src.gui import main_window
from src.app.db import create_tables

if __name__ == '__main__':
    create_tables()
    main_window.show_root()
