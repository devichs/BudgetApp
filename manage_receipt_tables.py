# manage_receipt_tables.py
import sqlite3
import csv
import os # Import os to construct relative paths

# Define the database name as a constant
DB_NAME = "receipts.sqlite"

# Define the path to the CSV file relative to this script's directory
# Assuming ui.csv is in the same directory as app.py and manage_receipt_tables.py
# If manage_receipt_tables.py is in the root, and ui.csv is also in the root:
CSV_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui.csv")
# If ui.csv is in a different location relative to your project root, adjust accordingly.
# For example, if your project root is the parent of where this script is:
# PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
# CSV_FILE_PATH = os.path.join(PROJECT_ROOT, "ui.csv") # Adjust if ui.csv is in a subfolder

def setup_database():
    """
    Initializes the database: creates tables if they don't exist
    and populates the uilookup table.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

         # Categories Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS categories(
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT NOT NULL UNIQUE,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Table 'categories' checked/created.")

        # Receipt_summaries table
        c.executescript("""
            create table if not exists receipt_summaries(
                summary_id integer not null primary key autoincrement,
                transaction_id integer not null unique,
                store text,
                purchase_date date,
                total_amount real,
                import_date datetime not null,
                last_modified_ts datetime not null default current_timestamp,
                foreign key (transaction_id) references transactions(transaction_id) on delete cascade
            );
        """)
        print("Table 'receipt_summaries' checked/created.")

        # Receipts Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS receipt_line_items(
                receipt_line_item_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                summary_id integer not null,
                description text not null,
                quantity integer not null,
                cost REAL not null,
                purchasedate DATE,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                foreign key (summary_id) references receipt_summaries(summary_id) on delete cascade
            );
        """)
        print("Table 'receipts' checked/created.")

        # Budget Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS budget(
                budget_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                amount REAL,
                budgetdate DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Table 'budget' checked/created.")

        # UILOOKUP Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS uilookup(
                uilookup_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                ui CHAR(2) NOT NULL UNIQUE,
                description TEXT,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Table 'uilookup' checked/created.")

        # Transactions Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS transactions(
                transaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                category_id INTEGER,
                core_account_id INTEGER,
                has_receipt integer not null default 0,
                notes TEXT,
                import_date DATETIME NOT NULL,
                last_modified_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories(category_id) on delete set null,
                FOREIGN KEY (core_account_id) REFERENCES core_accounts(core_account_id) 
            );
        """)
        print("Table 'transactions' (as primary) schema update.")

        c.executescript("""
        drop trigger if exists update_transactions_modtime;
        CREATE TRIGGER IF NOT EXISTS update_transactions_modtime
        AFTER UPDATE ON transactions FOR EACH ROW 
        BEGIN
            update transactions set last_modified_ts = CURRENT_TIMESTAMP where transaction_id = old.transaction_id;
        END;
        """ )
        print("Trigger 'update_transactions_modtime' re-applied.")

        # Core Accounts Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS  core_accounts(
                core_account_id integer primary key autoincrement,
                core_account_name text not null unique,
                core_account_type text,
                last_modified_ts datetime not null default current_timestamp
            );                    
        """)
        print("Table 'core_accounts' checked/created.")

        # Populate uilookup table (only if it's empty or using INSERT OR IGNORE)
        # Check if CSV file exists
        if not os.path.exists(CSV_FILE_PATH):
            print(f"Warning: CSV file for uilookup not found at {CSV_FILE_PATH}")
        else:
            print(f"Populating 'uilookup' from {CSV_FILE_PATH}...")
            try:
                with open(CSV_FILE_PATH, "r", encoding='utf-8') as csv_file_obj: # Specify encoding
                    reader = csv.reader(csv_file_obj)
                    # Skip header row if your CSV has one
                    # next(reader, None) 
                    
                    insert_sql = "INSERT OR IGNORE INTO uilookup(ui, description) VALUES (?, ?);"
                    rows_to_insert = []
                    for row in reader:
                        if len(row) >= 2: # Ensure row has at least two elements
                            rows_to_insert.append((row[0].strip(), row[1].strip()))
                        else:
                            print(f"Skipping malformed row in CSV: {row}")
                    
                    if rows_to_insert:
                        c.executemany(insert_sql, rows_to_insert)
                        print(f"Inserted/ignored {len(rows_to_insert)} rows into 'uilookup'.")
                    else:
                        print("No valid rows found in CSV to insert into 'uilookup'.")

            except FileNotFoundError:
                print(f"ERROR: Could not find the CSV file at {CSV_FILE_PATH}")
            except Exception as e:
                print(f"ERROR: Could not process CSV file {CSV_FILE_PATH}: {e}")


        conn.commit()
        print(f"Database '{DB_NAME}' setup complete.")

    except sqlite3.Error as e:
        print(f"SQLite error during database setup: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

# This allows the script to be run directly for setup if needed,
# but it won't run automatically when imported.
if __name__ == '__main__':
    print("Running database setup directly...")
    setup_database()