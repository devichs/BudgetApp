# BudgetApp called "What's Left!"
I started this project to work with a python web framework to start tracking grocery purchases by item. For instance, budgets
typically track total deductions, like the total grocery bill or total restaurant bill.  Nothing is itemized and therefore
individual item cost is not tracked. The idea here is to attempt to track the item cost over a period of time. Then, it might
be possible to compare item costs across different businesses. For example: the cost of a gallon of milk between Walmart, Aldi's and Kroger. This level of detail is generally not available.

## Application
This is a python web app using bottle and a sqlite db. 
Current functionality limited to setting a budget, adding purchases to a "receipt" list and, subtracting those receipts from the budget. 

## Page structure: 
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

## Requirements: 
1. python 3.9
2. bottle 3.8 (see bottlepy.org for more details)

## How to run: 
1. Create the database with manage_receipt_tables.py
	python .\manage_receipt_tables.py 
	
	Builds two tables, "reciepts" and "budget"

2. Run, python .\app.py

	Defaults to localhost:5555, go to your browser and type that address in. 

3. Manage your receipts and budget 

## ToDo: 
1. Build out Import Expense List.  This would be a .csv or other file type from a finance account to add to your expense list. 
2. Build out an OCR to text capability to scan receipts and load into the app.
3. Convert to virtenv.
