# BudgetApp called "What's Left!"
I started this project to work with a python web framework to start tracking grocery purchases by item. For instance, budgets
typically track total deductions, like the total grocery bill or total restaurant bill.  Nothing is itemized and therefore
individual item cost is not tracked. The idea here is to attempt to track the item cost over a period of time. Then, it might
be possible to compare item costs across different businesses. For example: the cost of a gallon of milk between Walmart, Aldi's and Kroger. This level of detail is generally not available.

## Application
This is a python web app using bottle and a sqlite db. 
Current functionality includes hand-typing the contents of a receipt and importing a csv file of transactions from a core account, i.e., checking, credit card. Setting and managing a budget amount. 

## Page structure: 
<pre>
Home(index)
Budget
	--Update Budget
	--Expense List
	--Home
Update Budget
	--Budget
	--Home
	--Cancel
Expense List
	--New Expense 
	--Budget 
	--Home 
	--Import Expense List [shell, future functionality]
Add Expense
	--Budget 
	--Expense list
	--Home 
	--Cancel
Import Transaction
	--Import From Account <name>
	--Account Type (optional) <type>
	--Select CSV file to import
	--Import Transactions

</pre>

## Requirements: 
1. python 3.9
2. bottle 1 or newer (see bottlepy.org for more details)

## How to run: 
1. Run, python .\app.py

	Defaults to localhost:5555, go to your browser and type that address in. 

3. Manage your receipts and budget and transactions 

## ToDo: 
1. Build out an OCR to text capability to scan receipts and load into the app.
2. Add report building and visualization processes.
3. AI to generate expense categories on the fly and per transaction.
