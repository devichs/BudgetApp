import sqlite3

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
ui text,
cost integer,
purchasedate date);
""")
con.commit()

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
con.commit()

"""
table name: whatsleft
A secondary table that provides the user a running total of 'What's Left' of their budget 
"""
c.executescript("""
create table if not exists budget(
id integer not null primary key unique,
)
