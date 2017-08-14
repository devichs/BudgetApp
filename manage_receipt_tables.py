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
ui char(2) NOT NULL,
cost integer,
purchasedate date,
FOREIGN KEY(ui) REFERENCES uilookup(ui));
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
table name: uilookup
This is a lookup table to provide a drop down menu of unit of issue
"""
c.executescript("""
create table if not exists uilookup(
id integer not null primary key unique,
ui char(2) NOT NULL,
description text);
""")
con.commit()

"""
insert the data into uilookup
"""
c.executescript("""
insert into uilookup(ui,description)values('AM','Ampoule');
insert into uilookup(ui,description)values('AT','Assortment');
insert into uilookup(ui,description)values('AY','Assembly');
insert into uilookup(ui,description)values('BA','Ball');
insert into uilookup(ui,description)values('BD','Bundle');
insert into uilookup(ui,description)values('BE','Bale');
insert into uilookup(ui,description)values('BF','Board Foot');
insert into uilookup(ui,description)values('BG','Bag');
insert into uilookup(ui,description)values('BK','Book');
insert into uilookup(ui,description)values('BL','Barrel');
insert into uilookup(ui,description)values('BO','Bolt');
insert into uilookup(ui,description)values('BQ','Briquet');
insert into uilookup(ui,description)values('BR','Bar');
insert into uilookup(ui,description)values('BT','Bottle');
insert into uilookup(ui,description)values('BX','Box');
insert into uilookup(ui,description)values('CA','Cartridge');
insert into uilookup(ui,description)values('CB','Carboy');
insert into uilookup(ui,description)values('CC','Cubic Centimeter');
insert into uilookup(ui,description)values('CD','Cubic Yard');
insert into uilookup(ui,description)values('CE','Cone');
insert into uilookup(ui,description)values('CF','Cubic Foot');
insert into uilookup(ui,description)values('CG','Centigram');
insert into uilookup(ui,description)values('CI','Cubic Inch');
insert into uilookup(ui,description)values('CK','Cake');
insert into uilookup(ui,description)values('CL','Coil');
insert into uilookup(ui,description)values('CM','Centimeter');
insert into uilookup(ui,description)values('CN','Can');
insert into uilookup(ui,description)values('CO','Container');
insert into uilookup(ui,description)values('CU','Curie');
insert into uilookup(ui,description)values('CY','Cylinder');
insert into uilookup(ui,description)values('RA','Ration');
insert into uilookup(ui,description)values('CZ','Cubic Meter');
insert into uilookup(ui,description)values('DC','Decagram');
insert into uilookup(ui,description)values('DE','Decimeter');
insert into uilookup(ui,description)values('DG','Decigram');
insert into uilookup(ui,description)values('DL','Deciliter');
insert into uilookup(ui,description)values('DM','Dram');
insert into uilookup(ui,description)values('DR','Drum');
insert into uilookup(ui,description)values('DW','Pennyweight');
insert into uilookup(ui,description)values('DZ','Dozen');
insert into uilookup(ui,description)values('EA','Each');
insert into uilookup(ui,description)values('EX','Exposure');
insert into uilookup(ui,description)values('FD','Fold');
insert into uilookup(ui,description)values('FR','Frame');
insert into uilookup(ui,description)values('FT','Foot');
insert into uilookup(ui,description)values('FV','Five');
insert into uilookup(ui,description)values('FY','Fifty');
insert into uilookup(ui,description)values('GG','Great Gross');
insert into uilookup(ui,description)values('GI','Gill');
insert into uilookup(ui,description)values('GL','Gallon');
insert into uilookup(ui,description)values('GM','Gram');
insert into uilookup(ui,description)values('GN','Grain');
insert into uilookup(ui,description)values('GP','Group');
insert into uilookup(ui,description)values('GR','Gross');
insert into uilookup(ui,description)values('HD','Hundred');
insert into uilookup(ui,description)values('HF','Hundred Feet');
insert into uilookup(ui,description)values('HK','Hank');
insert into uilookup(ui,description)values('HP','Hundred Pounds');
insert into uilookup(ui,description)values('HS','Hundred Square');
insert into uilookup(ui,description)values('HW','Hundred Weight');
insert into uilookup(ui,description)values('HY','Hundred Yards');
insert into uilookup(ui,description)values('IN','Inch');
insert into uilookup(ui,description)values('JR','Jar');
insert into uilookup(ui,description)values('KG','Kilogram');
insert into uilookup(ui,description)values('KM','Kilometer');
insert into uilookup(ui,description)values('KR','Carat');
insert into uilookup(ui,description)values('KT','Kit');
insert into uilookup(ui,description)values('LB','Pound');
insert into uilookup(ui,description)values('LF','Linear Foot');
insert into uilookup(ui,description)values('LG','Length');
insert into uilookup(ui,description)values('LI','Liter');
insert into uilookup(ui,description)values('LI','Liter');
insert into uilookup(ui,description)values('MC','Thousand Cubic');
insert into uilookup(ui,description)values('MC','Thousand');
insert into uilookup(ui,description)values('ME','Meal');
insert into uilookup(ui,description)values('MF','Thousand Feet');
insert into uilookup(ui,description)values('MG','Milligram');
insert into uilookup(ui,description)values('MI','Mile');
insert into uilookup(ui,description)values('ML','Milliliter');
insert into uilookup(ui,description)values('MM','Millimeter');
insert into uilookup(ui,description)values('MR','Meter');
insert into uilookup(ui,description)values('MX','Thousand');
insert into uilookup(ui,description)values('OT','Outfit');
insert into uilookup(ui,description)values('OZ','Ounce');
insert into uilookup(ui,description)values('PD','Pad');
insert into uilookup(ui,description)values('PG','Package');
insert into uilookup(ui,description)values('PI','Pillow');
insert into uilookup(ui,description)values('PM','Plate');
insert into uilookup(ui,description)values('PR','Pair');
insert into uilookup(ui,description)values('PT','Pint');
insert into uilookup(ui,description)values('PX','Pellet');
insert into uilookup(ui,description)values('PZ','Packet');
insert into uilookup(ui,description)values('QT','Quart');
insert into uilookup(ui,description)values('RD','Round');
insert into uilookup(ui,description)values('RL','Reel');
insert into uilookup(ui,description)values('RM','Ream');
insert into uilookup(ui,description)values('RO','Roll');
insert into uilookup(ui,description)values('RX','Thousand Rounds');
insert into uilookup(ui,description)values('SD','Skid');
insert into uilookup(ui,description)values('SE','Set');
insert into uilookup(ui,description)values('SF','Square Foot');
insert into uilookup(ui,description)values('SH','Sheet');
insert into uilookup(ui,description)values('SI','Square Inch');
insert into uilookup(ui,description)values('SK','Skein');
insert into uilookup(ui,description)values('SL','Spool');
insert into uilookup(ui,description)values('SM','Square Meter');
insert into uilookup(ui,description)values('SO','Shot');
insert into uilookup(ui,description)values('SP','Strip');
insert into uilookup(ui,description)values('SQ','Square');
insert into uilookup(ui,description)values('SX','Stick');
insert into uilookup(ui,description)values('SY','Square Yard');
insert into uilookup(ui,description)values('TD','Twenty-four');
insert into uilookup(ui,description)values('TE','Ten');
insert into uilookup(ui,description)values('TF','Twenty-five');
insert into uilookup(ui,description)values('TN','Ton (2,000 lb)');
insert into uilookup(ui,description)values('TO','Troy Ounce');
insert into uilookup(ui,description)values('TS','Thirty-six');
insert into uilookup(ui,description)values('TT','Tablet');
insert into uilookup(ui,description)values('TU','Tube');
insert into uilookup(ui,description)values('US','U.S.P. Unit');
insert into uilookup(ui,description)values('VI','Vial');
insert into uilookup(ui,description)values('YD','Yard');
""")
con.close()

