# routes.py

from bottle import route, view, run, template, request, static_file, error, get, post
from datetime import datetime
import sqlite3
import codecs
import os
import sys

# --- Import and call your database setup ---
import manage_receipt_tables
manage_receipt_tables.setup_database()
# -------------------------------------------

# Your existing database name constant can be used or you can refer to
# manage_receipt_tables.DB_NAME if you make it accessible from there.
# For simplicity, ensure your routes use the same DB_NAME.
DB_NAME = "receipts.sqlite" # Or manage_receipt_tables.DB_NAME

@route('/')
@route('/home')
@view('index')
def home():
    
    @route('/list')
    @view('list')
    def list():
        con = sqlite3.connect("receipts.sqlite")
        c = con.cursor()
        c.execute(""" 
        select id,store,category,item,quantity,ui,'$' || cast(cost as float) as cost,purchasedate,status from receipts
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

    
    @route('/edit/<receipt_id:int>', method='GET')
    @view('edit_receipt') 
    def show_edit_receipt_form(receipt_id):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT store, category, item, quantity, ui, cost, purchasedate,status FROM receipts WHERE id = ?", (receipt_id,))
        receipt_data = c.fetchone()
        c.close()
        conn.close()

        if receipt_data:
            return dict(
                no=receipt_id,
                old_data=receipt_data,

            )
        else:
            return "Receipt not found!"  
        
    @route('/edit/<receipt_id:int>', method='POST')
    def process_edit_receipt_form(receipt_id):
        store = request.forms.get('store').strip()
        category = request.forms.get('category').strip()
        item = request.forms.get('item').strip()
        quantity = request.forms.get('quantity').strip()
        ui = request.forms.get('ui').strip()
        cost = request.forms.get('cost').strip() # Should validate as float
        purchasedate = request.forms.get('purchasedate').strip() # Should validate as date
        # status = request.forms.get('status') # If you implement status

        # TODO: Validate data (e.g., cost is a number, date format is correct)

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            UPDATE receipts 
            SET store = ?, category = ?, item = ?, quantity = ?, ui = ?, cost = ?, purchasedate = ?
            WHERE id = ?
        """, (store, category, item, quantity, ui, float(cost), purchasedate, receipt_id)) # Add status if implemented
        conn.commit()
        c.close()
        conn.close()

        # return f"Receipt {receipt_id} updated. <a href='/list'>Back to list</a>"
        from bottle import redirect # make sure redirect is imported
        redirect('/list') # Redirect to the list page after successful update      
    
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

    @route('/import_transactions', method='GET')
    def show_import_form():
        return template('import_form') # Assuming your template is named import_form.tpl
    
    @route('/import_transactions', method='POST')
    def process_import():
        upload = request.files.get('csvfile')
        message = ""
    
        if not upload:
            message = "No file selected."
            return template('import_form', message=message)
    
        if not upload.filename.lower().endswith('.csv'):
            message = "Please upload a CSV file."
            return template('import_form', message=message)
    
        try:
            csv_content = upload.file.read().decode('utf-8')
            stream = io.StringIO(csv_content)
            reader = csv.DictReader(stream) # csv.DictReader is great for named columns!
    
            transactions_to_add = []
            imported_count = 0
            skipped_count = 0
            error_messages = []
    
            # --- Category Handling: Function to get or create category_id ---
            def get_or_create_category_id(category_name, db_cursor):
                category_name = category_name.strip()
                if not category_name:
                    return None # Or a default "Uncategorized" ID
    
                db_cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
                row = db_cursor.fetchone()
                if row:
                    return row[0]
                else:
                    # Category doesn't exist, create it
                    try:
                        db_cursor.execute("INSERT INTO categories (name) VALUES (?)", (category_name,))
                        # conn.commit() # Commit here or once after all categories
                        return db_cursor.lastrowid
                    except sqlite3.IntegrityError: # Should be caught by the SELECT first, but good for safety
                        db_cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
                        row = db_cursor.fetchone()
                        return row[0] if row else None
    
    
            # Get a cursor for database operations
            # Make sure 'conn' is your SQLite connection object
            c = conn.cursor()
    
            for row_number, row_data in enumerate(reader, start=1): # reader is now a DictReader
                try:
                    # --- Data Extraction and Cleaning ---
                    # Headers are: "Date", "Description", "Category", "Amount"
                    date_str = row_data.get("Date")
                    description = row_data.get("Description", "").strip() # .strip() to remove leading/trailing whitespace
                    category_name = row_data.get("Category", "").strip()
                    amount_str = row_data.get("Amount")
    
                    if not all([date_str, description, amount_str]): # Category can be optional
                        error_messages.append(f"Row {row_number}: Missing essential data (Date, Description, or Amount). Skipping.")
                        skipped_count += 1
                        continue
    
                    # --- Data Type Conversion & Validation ---
                    from datetime import datetime
                    try:
                        transaction_date = datetime.strptime(date_str.strip(), '%Y-%m-%d').strftime('%Y-%m-%d')
                    except ValueError:
                        error_messages.append(f"Row {row_number}: Invalid date format '{date_str}'. Expected YYYY-MM-DD. Skipping.")
                        skipped_count += 1
                        continue
    
                    try:
                        amount = float(amount_str.strip())
                    except ValueError:
                        error_messages.append(f"Row {row_number}: Invalid amount format '{amount_str}'. Skipping.")
                        skipped_count += 1
                        continue
    
                    # --- Get Category ID ---
                    category_id = None
                    if category_name: # Only process if category_name is present
                        category_id = get_or_create_category_id(category_name, c)
                        if category_id is None and category_name: # Failed to get/create valid ID
                            error_messages.append(f"Row {row_number}: Could not process category '{category_name}'. Assigning no category.")
                    # If you commit per category in get_or_create_category_id, ensure conn.commit() is called
    
                    # --- Prepare for Database Insertion ---
                    # TODO: Implement Duplicate Checking here if desired
                    # For example:
                    # c.execute("SELECT 1 FROM transactions WHERE transaction_date=? AND description=? AND amount=? AND category_id IS ?",
                    #           (transaction_date, description, amount, category_id)) # Adjust IS ? for category_id if it can be NULL
                    # if c.fetchone():
                    #     error_messages.append(f"Row {row_number}: Potential duplicate. Skipping: {date_str}, {description[:30]}, {amount}")
                    #     skipped_count += 1
                    #     continue
    
                    transactions_to_add.append(
                        (transaction_date, description, amount, category_id, "Imported") # Assuming 'notes' field exists
                    )
    
                except Exception as e_row:
                    error_messages.append(f"Row {row_number}: Error processing row '{row_data}'. Error: {e_row}. Skipping.")
                    skipped_count += 1
                    continue
    
            # --- Database Insertion ---
            if transactions_to_add:
                sql = "INSERT INTO transactions (transaction_date, description, amount, category_id, notes) VALUES (?, ?, ?, ?, ?)"
                try:
                    c.executemany(sql, transactions_to_add)
                    conn.commit() # Commit all transactions at once
                    imported_count = len(transactions_to_add)
                    message = f"{imported_count} transactions imported successfully. "
                except Exception as e_db:
                    conn.rollback() # Rollback on error
                    message = f"Database error during bulk insert: {e_db}. No transactions were imported in this batch."
                    # error_messages will contain per-row processing issues
            else:
                message = "No valid transactions found in the file to import. "
    
            if skipped_count > 0:
                message += f"{skipped_count} transactions were skipped. "
            if error_messages:
                # You might want to display these errors more nicely in your template
                message += "Details: " + " | ".join(error_messages[:5]) # Show first 5 errors for brevity
    
        except Exception as e_file:
            message = f"An error occurred reading or processing the file: {e_file}"
            import traceback
            traceback.print_exc() # For server-side logging
    
        return template('import_form', message=message) # Pass message back to the form