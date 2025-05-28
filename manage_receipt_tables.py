import sqlite3
import csv

"""
table name: receipts
The main table holding the receipt and purchase information
"""
con = sqlite3.connect("receipts.sqlite")
c = con.cursor()
c.executescript("""
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
c.executescript("""
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
c.executescript("""
create table if not exists uilookup(
id integer not null primary key unique,
ui char(2) NOT NULL,
description text);
""")
#con.commit()

"""
table name: transactions
This table is used to hold transactions imported from core accounts
"""
c.executescript("""
create table if not exists transacitons(
                id integer not null primary key autoincrement,
                transaction_date text not null,
                description text not null,
                amount real not null,
                category_id integer,
                notes text,
                created_at datetime default currrent_timestamp,
                foreign key (category_id) references categories(id)
                );
""")

"""
table name: categories
This table is used to hold categories for transactions
"""
c.executescript("""
                create table if not exists categories(
                id integer primary key autoincrement,
                name text not null unique
                );
""")
                
"""
insert the data into uilookup
"""

csv_file_path = "/Volumes/AllShare/VadaPav/git/BudgetApp/ui.csv"

with open(csv_file_path,"r") as cvs_file:
    reader = csv.reader(cvs_file)

    for row in reader:
        row1 = row[0]
        row2 = row[1]
        insertSql = (f"insert into uilookup(ui,description) values ({row1},{row2});")
        #print(insertSql)
        c.execute(insertSql)

con.commit();
if con:
    con.close();
