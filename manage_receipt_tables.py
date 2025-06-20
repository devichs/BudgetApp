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
            CREATE TABLE IF NOT EXISTS main_categories(
                main_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                main_category_name TEXT NOT NULL UNIQUE,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        print("Table 'main_categories' checked/created.")

        # seed main_categories

        main_categories_to_seed = [
            'Recurring-Fixed'
            ,'Recurring-NotFixed'
            ,'Discretionary-NotRecurring'
        ]

        c.executemany(
            "insert or ignore into main_categories (main_category_name) values (?)",
            [(cat,) for cat in main_categories_to_seed]
        )
        print("Main categories seeded.")

        c.executescript("""
            CREATE TABLE IF NOT EXISTS sub_categories(
                sub_category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sub_category_name TEXT NOT NULL UNIQUE,
                main_category_id integer not null,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                unique(sub_category_name,main_category_id),
                foreign key (main_category_id) references main_categories(main_category_id)
            );
        """)
        print("Table 'sub_categories' checked/created.")

        # seed categories table if needed
        core_sub_categories = [
			'AmazonPurchase'
			,'AppleServicesPayment'
			,'AtmWithdrawal'
			,'BankDeposit'
			,'BankTransfer'
			,'CarExpense'
			,'CarGas'
			,'CarInsurancePayemnt'
			,'CarParking'
			,'CashedCheck'
			,'ClothingPurchase'
			,'CollegeFundDeposit'
			,'CreditCardCredit'
			,'CreditCardPayment'
			,'Dentist'
			,'Discretionary-NotRecurring'            
			,'EducationExpense'
			,'Entertainment'
			,'FastFood'
			,'Groceries'
			,'HomeRepair'
			,'Income-Paycheck'
			,'InternetServicePayment'
			,'InterestIncome'
			,'MobilePhonePlanPayment'
			,'MortgagePayment'
			,'MusicLessons'
			,'PersonalCare'
			,'Pharmacy'
			,'PostOffice'
			,'PurchaseReturnCredit'
			,'Recurring-Fixed'
			,'Recurring-NotFixed'
			,'Restaurants'
			,'RoadToll'
			,'Shopping'
			,'SportsClubMembership'
			,'StreamingServices'
			,'Taxi'
			,'Travel'
			,'Utilities'
		]
        c.executemany(
			    "insert or ignore into sub_categories (sub_category_name) values (?)", [(category,) for category in core_sub_categories]
			    )
        print(f"Core sub_categories seeded/verified.")
        
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

        # Receipts Line Items Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS receipt_line_items(
                receipt_line_item_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                summary_id integer not null,
                description text not null,
                quantity integer not null,
                cost REAL not null,
                purchasedate DATE,
                sub_category_id integer,
                last_modified_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
                foreign key (summary_id) references receipt_summaries(summary_id) on delete cascade,
                foreign key (sub_category_id) references sub_categories(sub_category_id) on delete set null
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

        # Transactions Table
        c.executescript("""
            CREATE TABLE IF NOT EXISTS transactions(
                transaction_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                transaction_date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                sub_category_id INTEGER,
                core_account_id INTEGER,
                has_receipt integer not null default 0,
                notes TEXT,
                import_date DATETIME NOT NULL,
                last_modified_ts DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sub_category_id) REFERENCES sub_categories(sub_category_id) on delete set null,
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