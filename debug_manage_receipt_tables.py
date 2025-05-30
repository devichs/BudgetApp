import sqlite3
import os

# Check if the database file exists
db_file = "receipts.sqlite"

if os.path.exists(db_file):
    os.remove(db_file)
    print("The file has been removed")
else:
    print("The file does not exist")

"""
table name: receipts
The main table holding the receipt and purchase information
"""
con = sqlite3.connect("/Volumes/AllShare/VadaPav/git/BudgetApp/receipts.sqlite")
c = con.cursor()
c.execute("""
create table if not exists receipts(
id integer not null primary key unique,
store text,
category text,
item text,
quantity text,
ui char(2) NOT NULL,
cost integer,
purchasedate date);
""")
#con.commit()

"""
table name: budget
The secondary table that takes user input as the budgetted amount
and then subtracts the running total of purchases to give the user 'What's Left'
"""
c.execute("""
create table if not exists budget(
id integer not null primary key unique,
amount integer,
budgetdate datetime default current_timestamp);
""")
#con.commit()

"""
table name: uilookup
This is a lookup table to provide a drop down menu of unit of issue
"""
c.execute("""
create table if not exists uilookup(
id integer not null primary key unique,
ui char(2) NOT NULL,
description text);
""")
#con.commit()

c.execute("""select name from sqlite_master where type='table';""")
tables = c.fetchall()

print("tables built: ")
for table in tables:
    print(table[0])
"""
insert the data into uilookup
"""
if con:
    print("Connected to the database")
else:
    print("Not connected to the database")

import csv

csv_file_path = "/Volumes/AllShare/VadaPav/git/BudgetApp/ui.txt"

with open(csv_file_path,"r") as cvs_file:
    reader = csv.reader(cvs_file)

    for row in reader:
        row1 = row[0]
        row2 = row[1]
        insertSql = (f"insert into uilookup(ui,description) values ({row1},{row2});")
        print(insertSql)
        c.execute(insertSql)

con.commit();
if con:
    con.close();

