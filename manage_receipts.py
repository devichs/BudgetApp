from bottle import route, run, template, request, static_file, error,get,post
import sqlite3
import cherrypy
import codecs
import os
import sys

@route("/<filename>")
def sf(filename):
	return static_file(filename,root = ".\\")

@route("/index")
def index():
	output = template("index")
	return output

@route("/list")
def results_list():
	con = sqlite3.connect("receipts.sqlite")
	c = con.cursor()
	c.execute("""
	select * from receipts
	""")
	result = c.fetchall()
	output = template("list",rows = result)
	return output
	
@route("/new",method = "GET")
def new_item():
	if request.GET.get("save","").strip():
		newStore = request.GET.get("store","").strip()
		newCategory = request.GET.get("category","").strip()
		newItem = request.GET.get("item","").strip()
		newQuantity = request.GET.get("quantity","").strip()
		newUi = request.GET.get("ui","").strip()
		newCost = request.GET.get("cost","").strip()
		newPurchasedate = request.GET.get("purchasedate","").strip()
		con = sqlite3.connect("receipts.sqlite")
		c = con.cursor()
		c.execute("""
		insert into receipts(store,category,item,quantity,ui,cost,purchasedate)values(?,?,?,?,?,?,?)""",(newStore,newCategory,newItem,newQuantity,newUi,newCost,newPurchasedate,))
		new_id = c.lastrowid 
		con.commit()
		c.close()
		url = "http://localhost:8080/list"
		return"<p>The new receipt was inserted into the database, the ID is {0} </p><p><a href = http://localhost:8080/list>List</a></p><p><a href = http://localhost:8080/new>New Expense</a></p>".format(new_id)
	else:
		return template("new_receipt.tpl")
		
@route("/budget")
def  budget():
	con = sqlite3.connect("receipts.sqlite")
	c = con.cursor()
	c.execute("""
	select distinct '$' || amount, date(budgetdate) as 'DateSet','$' || r.cost as 'ExpensesTotal','$' || cast((x.budget - r.cost) as float) as 'WhatsLleft'
        from budget b,
        (select sum(cost)cost from receipts)r,
	(select distinct amount as budget,id  from budget where id in (
	select max(id) from budget))x
	where b.id in (
	select max(id) from budget)
	order by b.budgetdate desc	
	""")
	result = c.fetchall()	
	output = template("budget",rows = result)
	return output
	
@route("/newbudget",method = "GET")
def new_budget():
	if request.GET.get("update","").strip():
		newAmount = request.GET.get("amount","").strip()
		con = sqlite3.connect("receipts.sqlite")
		c = con.cursor()
		c.execute("""
		insert into budget(amount)values(?)""",(newAmount,))
		new_id = c.lastrowid 
		con.commit()
		c.close()
		return"<p>The new budget amount was inserted into the database, the ID is {0} </p></p><a href = http://localhost:8080/budget>Budget</a>".format(new_id)
	else: 
		return template("new_budget.tpl")
				
if __name__ == "__main__":
	run(host = "localhost",port = 8080,reloader = True,server = "cherrypy",debug = True)
	
	""" whatsleft calculation
	select cast((x.budget - r.cost) as float) as whatsleft
	from 
	(select sum(cost)cost from receipts)r,
	(select distinct amount as budget,id  from budget where id in (
	select max(id) from budget))x
"""
	
	