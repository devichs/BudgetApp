import pytesseract
from PIL import Image
import sqlite3

pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

db_file = "receipt_data.sqlite"
table_name = "scanned_receipts"

image_path = "/Volumes/AllShare/VadaPav/git/BudgetApp/receipts/receiptScan1.jpg"
image = Image.open(image_path)
raw_text = pytesseract.image_to_string(image)
print("Extracted Text: \n", raw_text)
    
lines = raw_text.split("\n")
rows = []
for line in lines: 
    columns = line.split(" ")
    print(columns)
    raw_receipt = columns

# Raw receipt output
'''
raw_receipt = [
    ['BreadButter-Valparaiso'],
    [''],
    ['98', '5', 'John', 'Sims', 'Pwky', 'Jan', '16,', '2025'],
    ['Valparaiso,', 'FL', '32580', '3:06', 'PM'],
    ['(850)', '964-1920', 'Anh', 'Thu'],
    ['Ticket:', '#41'],
    [''],
    ['Receipt:', '3RT8'],
    ['Mango', 'Milk', 'Tea', '=', '1', '$5.50'],
    ['Tapioca', 'Boba', '($0.75),', 'Medium,'],
    [''],
    ['Regular', 'Sweet'],
    [''],
    ['Subtotal', '$5.50'],
    [''],
    ['Sale', 'Tax', '$0.38'],
    ['Total', '$5.88'],
    ['Cash', '$10.00'],
    [''],
    ['Change', '$4.12'],
    ['']
]
'''

# Step 1: Parse the raw data
store_name = raw_receipt[0]
print(store_name)
date_time = " ".join(raw_receipt[2][-3:])  # Example: 'Jan 16, 2025'
items = []
totals = {}

for line in raw_receipt:
    if '=' in line:  # Identify items
        item_name = " ".join(line[:-3])  # Join all but last 3 elements
        quantity = int(line[-3])
        price = float(line[-1].strip('$'))
        items.append((item_name, quantity, price))
    elif 'Subtotal' in line:
        totals['subtotal'] = float(line[1].strip('$'))
    elif 'Sale Tax' in line:
        totals['tax'] = float(line[2].strip('$'))
    elif 'Total' in line:
        totals['total'] = float(line[1].strip('$'))
    elif 'Cash' in line:
        totals['cash'] = float(line[1].strip('$'))
    elif 'Change' in line:
        totals['change'] = float(line[1].strip('$'))

# Step 2: Insert data into SQLite
db_file = "receipt_data.sqlite"
con = sqlite3.connect(db_file)
c = con.cursor()

# Create tables
c.execute("""
    CREATE TABLE IF NOT EXISTS store (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        date_time TEXT
    );
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER,
        item_name TEXT,
        quantity INTEGER,
        price REAL,
        FOREIGN KEY (store_id) REFERENCES store (id)
    );
""")
c.execute("""
    CREATE TABLE IF NOT EXISTS totals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER,
        subtotal REAL,
        tax REAL,
        total REAL,
        cash REAL,
        change REAL,
        FOREIGN KEY (store_id) REFERENCES store (id)
    );
""")

# Insert store information
c.execute("INSERT INTO store (name, date_time) VALUES (?, ?);", (store_name, date_time))
store_id = c.lastrowid

# Insert items
for item in items:
    c.execute("INSERT INTO items (store_id, item_name, quantity, price) VALUES (?, ?, ?, ?);", (store_id, item[0], item[1], item[2]))

# Insert totals
c.execute("INSERT INTO totals (store_id, subtotal, tax, total, cash, change) VALUES (?, ?, ?, ?, ?, ?);", (
    store_id,
    totals.get('subtotal'),
    totals.get('tax'),
    totals.get('total'),
    totals.get('cash'),
    totals.get('change')
))

# Commit and close
con.commit()
con.close()

print("Receipt data successfully loaded into the database.")


'''
Extracted Text: 
 BreadButter-Valparaiso

98 5 John Sims Pwky Jan 16, 2025
Valparaiso, FL 32580 3:06 PM
(850) 964-1920 Anh Thu
Ticket: #41

Receipt: 3RT8
Mango Milk Tea = 1 $5.50
Tapioca Boba ($0.75), Medium,

Regular Sweet

Subtotal $5.50

Sale Tax $0.38
Total $5.88
Cash $10.00

Change $4.12
'''

