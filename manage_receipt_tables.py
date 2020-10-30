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
cost decimal(10,5),
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
insert into uilookup(ui,description)values('AM','AM - Ampoule');
insert into uilookup(ui,description)values('AT','AT - Assortment');
insert into uilookup(ui,description)values('AY','AY - Assembly');
insert into uilookup(ui,description)values('BA','BA - Ball');
insert into uilookup(ui,description)values('BD','BD - Bundle');
insert into uilookup(ui,description)values('BE','BE - Bale');
insert into uilookup(ui,description)values('BF','BF - Board Foot');
insert into uilookup(ui,description)values('BG','BG - Bag');
insert into uilookup(ui,description)values('BK','BK - Book');
insert into uilookup(ui,description)values('BL','BL - Barrel');
insert into uilookup(ui,description)values('BO','BO - Bolt');
insert into uilookup(ui,description)values('BQ','BQ - Briquet');
insert into uilookup(ui,description)values('BR','BR - Bar');
insert into uilookup(ui,description)values('BT','BT - Bottle');
insert into uilookup(ui,description)values('BX','BX - Box');
insert into uilookup(ui,description)values('CA','CA - Cartridge');
insert into uilookup(ui,description)values('CB','CB - Carboy');
insert into uilookup(ui,description)values('CC','CC - Cubic Centimeter');
insert into uilookup(ui,description)values('CD','CD - Cubic Yard');
insert into uilookup(ui,description)values('CE','CE - Cone');
insert into uilookup(ui,description)values('CF','CF - Cubic Foot');
insert into uilookup(ui,description)values('CG','CG - Centigram');
insert into uilookup(ui,description)values('CI','CI - Cubic Inch');
insert into uilookup(ui,description)values('CK','CK - Cake');
insert into uilookup(ui,description)values('CL','CL - Coil');
insert into uilookup(ui,description)values('CM','CM - Centimeter');
insert into uilookup(ui,description)values('CN','CN - Can');
insert into uilookup(ui,description)values('CO','CO - Container');
insert into uilookup(ui,description)values('CU','CU - Curie');
insert into uilookup(ui,description)values('CY','CY - Cylinder');
insert into uilookup(ui,description)values('CZ','CZ - Cubic Meter');
insert into uilookup(ui,description)values('DC','DC - Decagram');
insert into uilookup(ui,description)values('DE','DE - Decimeter');
insert into uilookup(ui,description)values('DG','DG - Decigram');
insert into uilookup(ui,description)values('DL','DL - Deciliter');
insert into uilookup(ui,description)values('DM','DM - Dram');
insert into uilookup(ui,description)values('DR','DR - Drum');
insert into uilookup(ui,description)values('DW','DW - Pennyweight');
insert into uilookup(ui,description)values('DZ','DZ - Dozen');
insert into uilookup(ui,description)values('EA','EA - Each');
insert into uilookup(ui,description)values('EX','EX - Exposure');
insert into uilookup(ui,description)values('FD','FD - Fold');
insert into uilookup(ui,description)values('FR','FR - Frame');
insert into uilookup(ui,description)values('FT','FT - Foot');
insert into uilookup(ui,description)values('FV','FV - Five');
insert into uilookup(ui,description)values('FY','FY - Fifty');
insert into uilookup(ui,description)values('GG','GG - Great Gross');
insert into uilookup(ui,description)values('GI','GI - Gill');
insert into uilookup(ui,description)values('GL','GL - Gallon');
insert into uilookup(ui,description)values('GM','GM - Gram');
insert into uilookup(ui,description)values('GN','GN - Grain');
insert into uilookup(ui,description)values('GP','GP - Group');
insert into uilookup(ui,description)values('GR','GR - Gross');
insert into uilookup(ui,description)values('HD','HD - Hundred');
insert into uilookup(ui,description)values('HF','HF - Hundred Feet');
insert into uilookup(ui,description)values('HK','HK - Hank');
insert into uilookup(ui,description)values('HP','HP - Hundred Pounds');
insert into uilookup(ui,description)values('HS','HS - Hundred Square');
insert into uilookup(ui,description)values('HW','HW - Hundred Weight');
insert into uilookup(ui,description)values('HY','HY - Hundred Yards');
insert into uilookup(ui,description)values('IN','IN - Inch');
insert into uilookup(ui,description)values('JR','JR - Jar');
insert into uilookup(ui,description)values('KG','KG - Kilogram');
insert into uilookup(ui,description)values('KM','KM - Kilometer');
insert into uilookup(ui,description)values('KR','KR - Carat');
insert into uilookup(ui,description)values('KT','KT - Kit');
insert into uilookup(ui,description)values('LB','LB - Pound');
insert into uilookup(ui,description)values('LF','LF - Linear Foot');
insert into uilookup(ui,description)values('LG','LG - Length');
insert into uilookup(ui,description)values('LI','LI - Liter');
insert into uilookup(ui,description)values('LI','LI - Liter');
insert into uilookup(ui,description)values('MC','MC - Thousand Cubic');
insert into uilookup(ui,description)values('MC','MC - Thousand');
insert into uilookup(ui,description)values('ME','ME - Meal');
insert into uilookup(ui,description)values('MF','MF - Thousand Feet');
insert into uilookup(ui,description)values('MG','MG - Milligram');
insert into uilookup(ui,description)values('MI','MI - Mile');
insert into uilookup(ui,description)values('ML','ML - Milliliter');
insert into uilookup(ui,description)values('MM','MM - Millimeter');
insert into uilookup(ui,description)values('MR','MR - Meter');
insert into uilookup(ui,description)values('MX','MX - Thousand');
insert into uilookup(ui,description)values('OT','OT - Outfit');
insert into uilookup(ui,description)values('OZ','OZ - Ounce');
insert into uilookup(ui,description)values('PD','PD - Pad');
insert into uilookup(ui,description)values('PG','PG - Package');
insert into uilookup(ui,description)values('PI','PI - Pillow');
insert into uilookup(ui,description)values('PM','PM - Plate');
insert into uilookup(ui,description)values('PR','PR - Pair');
insert into uilookup(ui,description)values('PT','PT - Pint');
insert into uilookup(ui,description)values('PX','PX - Pellet');
insert into uilookup(ui,description)values('PZ','PZ - Packet');
insert into uilookup(ui,description)values('QT','QT - Quart');
insert into uilookup(ui,description)values('RA','RA - Ration');
insert into uilookup(ui,description)values('RD','RD - Round');
insert into uilookup(ui,description)values('RL','RL - Reel');
insert into uilookup(ui,description)values('RM','RM - Ream');
insert into uilookup(ui,description)values('RO','RO - Roll');
insert into uilookup(ui,description)values('RX','RX - Thousand Rounds');
insert into uilookup(ui,description)values('SD','SD - Skid');
insert into uilookup(ui,description)values('SE','SE - Set');
insert into uilookup(ui,description)values('SF','SF - Square Foot');
insert into uilookup(ui,description)values('SH','SH - Sheet');
insert into uilookup(ui,description)values('SI','SI - Square Inch');
insert into uilookup(ui,description)values('SK','SK - Skein');
insert into uilookup(ui,description)values('SL','SL - Spool');
insert into uilookup(ui,description)values('SM','SM - Square Meter');
insert into uilookup(ui,description)values('SO','SO - Shot');
insert into uilookup(ui,description)values('SP','SP - Strip');
insert into uilookup(ui,description)values('SQ','SQ - Square');
insert into uilookup(ui,description)values('SX','SX - Stick');
insert into uilookup(ui,description)values('SY','SY - Square Yard');
insert into uilookup(ui,description)values('TD','TD - Twenty-four');
insert into uilookup(ui,description)values('TE','TE - Ten');
insert into uilookup(ui,description)values('TF','TF - Twenty-five');
insert into uilookup(ui,description)values('TN','TN - Ton (2,000 lb)');
insert into uilookup(ui,description)values('TO','TO - Troy Ounce');
insert into uilookup(ui,description)values('TS','TS - Thirty-six');
insert into uilookup(ui,description)values('TT','TT - Tablet');
insert into uilookup(ui,description)values('TU','TU - Tube');
insert into uilookup(ui,description)values('US','US - U.S.P. Unit');
insert into uilookup(ui,description)values('VI','VI - Vial');
insert into uilookup(ui,description)values('YD','YD - Yard');
""")
con.close()

