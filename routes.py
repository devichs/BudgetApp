"""
Routes and views for the bottle application.
"""

from bottle import route, view, run, template, request, static_file, error,get,post
from datetime import datetime
import sqlite3
import codecs 
import os 
import sys 

@route('/')
@route('/home')
@view('index')
def home():
    """Renders the home page."""
    return dict(
        year=datetime.now().year
    )

@route('/list')
@view('list')
def list():
    con = sqlite3.connect("receipts.sqlite")
    c = con.cursor()
    c.execute("""
    select id,store,category,item,quantity,ui,'$' || cast(cost as float) as cost,purchasedate from receipts
    """)
    result = c.fetchall()
    output = template("list",rows = result)
    return output

@route("/budget")
def  budget():
	con = sqlite3.connect("receipts.sqlite")
	c = con.cursor()
	c.execute("""
	select distinct '$' || cast(amount as float) as 'amount', date(budgetdate) as 'DateSet','$' || r.cost as 'ExpensesTotal','$' || cast((x.budget - r.cost) as float) as 'WhatsLleft'
        from budget b,
        (select sum(cost)cost from receipts where purchasedate >= (select max(date(budgetdate)) from budget))r,
	(select distinct amount as budget,id  from budget where id in (
	select max(id) from budget))x
	where b.id in (
	select max(id) from budget) 
	order by b.budgetdate desc	
	""")
	result = c.fetchall()	
	output = template("budget",rows = result)
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
		url = "http://localhost:5555/list"
		return"<p>The new receipt was inserted into the database, the ID is {0} </p><p><a href = http://localhost:5555/list>List</a></p><p><a href = http://localhost:5555/new>New Expense</a></p>".format(new_id)
	else:
		return template("new_receipt.tpl")

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
		return"<p>The new budget amount was inserted into the database, the ID is {0} </p></p><a href = http://localhost:5555/budget>Budget</a>".format(new_id)
	else: 
		return template("new_budget.tpl")