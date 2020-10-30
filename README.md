# BudgetApp called "What's Left!"
I got into this project to work with a python web framework and see if I could start tracking grocery purchases by item.
This is a python web app using bottle and a sqlite db. 
Current functionality limited to setting a budget, adding purchases to a "receipt" list and, subtracting those receipts from the budget. 

Page structure: 
<pre>
Home(index)
--Budget
	--Update Budget
	--Expense List
	--Home
--Update Budget
	--Budget
	--Home
	--Cancel
--Expense List
	--New Expense 
	--Budget 
	--Home 
	--Import Expense List [shell, future functionality]
--Add Expense
	--Budget 
	--Expense list
	--Home 
	--Cancel
</pre>

Requirements: 
Works with python 3.6 and >, bottle 12.13 and >

How to run: 
1. Create the database with manage_receipt_tables.py
	python .\manage_receipt_tables.py 
	
	Builds two tables, "reciepts" and "budget"

2. Run, python .\app.py

	Defaults to localhost:5555, go to your browser and type that address in. 

3. Manage your receipts and budget 

ToDo 
[Future]: 
1. Build out Import Expense List.  This would be a .csv or other file type from a finance account to add to your expense list. 
2. Build out an OCR to text capability to scan receipts and load into the app.
