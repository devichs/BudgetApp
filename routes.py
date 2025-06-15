# routes.py

from bottle import route, view, run, template, request, static_file, error, get, post, redirect, response
from datetime import datetime
import sqlite3
import codecs
import os
import sys
import csv
import io
from datetime import datetime
import math
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import tempfile
import re
from dateutil.parser import parse
import json

# function to extract scanned receipt details
def extract_receipt_details(text):

    details = {
        'store_name': None,
        'purchase_date': None,
        'total_amount': None
    }

    total_match = re.search(r'^Total\s+\$?(\d+\.\d{2})', text, re.IGNORECASE | re.MULTILINE)
    if total_match:
        details['total_amount'] = float(total_match.group(1))

    date_pattern = re.compile(
        r'(\d{1,2}[/\.-]\d{1,2}[/\.-]\d{2,4})|'  # Matches DD/MM/YYYY, DD-MM-YYYY, etc.
        r'(\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b\s+\d{1,2},?\s+\d{4})' # Matches "Jan 16, 2025"
    , re.IGNORECASE)

    for line in text.splitlines():
        match = date_pattern.search(line)
        if match:
            try:
                date_string = match.group(0)
                parsed_date = parse(date_string)
                details['purchase_date'] = parsed_date.strftime('%Y-%m-%d')
                print(f"Found and parsed date:  {details['purchase_date']}")
                break
            except (ValueError, TypeError):
                continue

    lines = text.splitlines()
    for line in lines:
        if line.strip(): # Find the first line with actual content
            details['store_name'] = line.strip()
            break

    return details

    # end parse data for scanning receipts

# --- Import and call database ---
import manage_receipt_tables
manage_receipt_tables.setup_database()
# -------------------------------------------

DB_NAME = "receipts.sqlite"

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
        select receipts_id,store,c.category_name,item,quantity,ui,'$' || cast(cost as float) as cost,purchasedate,status 
        from receipts r
        join categories c on c.category_id = r.category_id
        """)

        result = c.fetchall()
        output = template("list",rows = result)
        return output
   
    @route("/budget")
    @view("budget")
    def  unified_budget_view():
        today = datetime.now()
        start_of_month = today.strftime('%Y-%m-01')
        end_of_month = today .strftime('%Y-%m-%d')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            select sum(amount)
            from transactions
            where amount > 0 and transaction_date >= ? and transaction_date <= ?            
        """, (start_of_month,end_of_month))
        total_income_result = c.fetchone() [0]
        total_income = total_income_result if total_income_result is not None else 0.0

        c.execute("""
            select sum(amount)
            from transactions
            where amount < 0 and transaction_date >= ? and transaction_date <= ?
        """,(start_of_month,end_of_month))
        transactions_expenses_result = c.fetchone()[0]
        transactions_expenses = transactions_expenses_result if transactions_expenses_result is not None else 0.0

        c.execute("""
            select sum(r.cost)
            from receipts as r
            join receipt_summaries as rs on r.summary_id = rs.summary_id
            where rs.purchase_date >= ? and rs.purchase_date <= ?
        """, (start_of_month,end_of_month))
        receipts_expenses_result = c.fetchone()[0]
        receipts_expenses = receipts_expenses_result if receipts_expenses_result is not None else 0.0

        total_expenses = abs(transactions_expenses) + receipts_expenses

        conn.close()

        whats_left = total_income - total_expenses

        return dict(
            title = f"Budget Summary for {today.strftime('%B %Y')}",
            start_date = start_of_month,
            end_date = end_of_month,
            total_income = total_income,
            total_expenses = total_expenses,
            whats_left = whats_left
        )
    
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
        c.execute("SELECT store, category, item, quantity, ui, cost, purchasedate,status FROM receipts WHERE receipts_id = ?", (receipt_id,))
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
        cost = request.forms.get('cost').strip() 
        purchasedate = request.forms.get('purchasedate').strip() 

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            UPDATE receipts 
            SET store = ?, category = ?, item = ?, quantity = ?, ui = ?, cost = ?, purchasedate = ?
            WHERE receipts_id = ?
        """, (store, category, item, quantity, ui, float(cost), purchasedate, receipt_id)) # Add status if implemented
        conn.commit()
        c.close()
        conn.close()

        from bottle import redirect 
        redirect('/list')     
    
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
    @view('import_transactions_form')
    def show_import_form():
        return dict()
    
    # begin csv file import process

    def get_or_create_categories_id(category_name,db_cursor):
        category_name = category_name.strip()
        if not category_name:
            return None
        db_cursor.execute("select category_id from categories where category_name = ?",(category_name,))
        row = db_cursor.fetchone()
        if row:
            return row[0]
        else:
            db_cursor.execute("insert into categories (category_name) values (?)",(category_name,))
            return db_cursor.lastrowid

    def get_or_create_core_account_id(account_name,account_type,db_cursor):
        account_name = account_name.strip()
        account_type = account_type.strip()
        if not account_name:
            return None
        
        db_cursor.execute("select core_account_id from core_accounts where core_account_name = ?", (account_name,))
        row = db_cursor.fetchone()
        if row:
            return row[0]
        else:
            db_cursor.execute("insert into core_accounts(core_account_name,core_account_type) values(?,?)", (account_name,account_type,))
            return db_cursor.lastrowid

    @route('/import_transactions', method='POST')
    def do_import_transactions():
        upload = request.files.get('csvfile')
        account_name = request.forms.get('core_account_name')
        account_type = request.forms.get('core_account_type')

        if not upload or not upload.filename.lower().endswith('.csv'):
            return template('import_transactions_form', error_message = "Upload must be a valid csv file.")
        if not account_name or not account_name.strip():
            return template('import_transactions_form', error_message="The 'Import From Account' name is required.")

        try:
            csv_content = upload.file.read().decode('utf-8')
            stream = io.StringIO(csv_content)
            reader = csv.DictReader(stream)
        except Exception as e:
            return template('import_transactions_form', error_message = f"Error reading or decoding file: {e}")
        
        import_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        core_account_id = get_or_create_core_account_id(account_name,account_type,c)

        batch_category_cache = {}

        transacations_to_add = []
        skipped_count = 0
        imported_count = 0
        processing_errors = []

        for row_number, row in enumerate(reader, start=2):
            try:
                date_str = row.get("Date", "").strip()
                description = row.get("Description", "").strip()
                category_name = row.get("Category", "").strip()
                amount_str = row.get("Amount", "").strip()
	
                if not all([date_str, description, amount_str]):
                    processing_errors.append(f"Row {row_number}: Missing essential data (Date, Description, or Amount).")
                    skipped_count += 1
                    continue

                # add intelligent guess for null category during import
                if not category_name:
                    guessed_category = None

                    search_keyword = description.split(' ')[0]

                    if category_name and search_keyword:
                        batch_category_cache[search_keyword] = category_name

                    if not category_name and search_keyword:
                        guessed_category = None

                    if search_keyword in batch_category_cache:
                        guessed_category = batch_category_cache[search_keyword]
                        print(f"Row {row_number}: Guessed category '{guessed_category}' for '{description}' from this batch.")
                    else:
                        c.execute("""
                                  select cat.category_name
                                  from transactions t
                                  join categories cat on t.category_id = cat.category_id
                                  where t.description like ? and t.category_id is not null
                                  order by t.import_date desc
                                  limit 1
                                  """, ('%' + search_keyword + '%',))
                        
                        result = c.fetchone()
                        if result:
                            guessed_category = result[0]
                            print(f"Row {row_number}: Guessed category '{guessed_category}' for description '{description}'")

                    if guessed_category:
                            category_name = guessed_category
                    else:
                        category_name = description
                        print(f"Row {row_number}: No similar category found for '{description}'. Creating new category.")

                        # end category guessing  

                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    transaction_date = date_str
                except ValueError:
                    processing_errors.append(f"Row {row_number}: Invalid date format '{date_str}'. Expected YYYY-MM-DD.")
                    skipped_count  += 1
                    continue

                try:
                    cleaned_amount_str = amount_str.replace(',','')
                    amount = float(cleaned_amount_str)
                except ValueError:
                    processing_errors.append(f"Row {row_number}: Invalid amount format '{amount_str}'.")
                    skipped_count += 1
                    continue

                category_id = get_or_create_categories_id(category_name,c)

                c.execute("select 1 from transactions where transaction_date = ? and description = ? and amount = ?", (transaction_date,description,amount))
                if c.fetchone():
                    skipped_count += 1
                    continue

                transacations_to_add.append({
                    "date": transaction_date,
                    "description": description,
                    "amount": amount,
                    "category_id": category_id, 
                    "core_account_id": core_account_id,
                    "notes": "Imported",
                    "import_date": import_timestamp
                })
                imported_count += 1

            except Exception as e:
                processing_errors.append(f"Row {row_number}: Unexpected error - {e}")
                skipped_count += 1 
                continue

        if transacations_to_add:
            sql = "insert into transactions (transaction_date,description,amount,category_id,core_account_id,notes,import_date) values (?,?,?,?,?,?,?)"
            insert_data = [(tx['date'],tx['description'],tx['amount'],tx['category_id'],tx['core_account_id'],tx['notes'],tx['import_date']) for tx in transacations_to_add]
            c.executemany(sql,insert_data)
            imported_count = len(transacations_to_add)

        conn.commit()
        conn.close()

        final_message = f"File import complete! Successfully imported {imported_count} new transactions."
        if skipped_count > 0:
            final_message += f" Skipped {skipped_count} existing or invalid rows."
        if processing_errors:
            final_message += f" Errors encountered: {'; '.join(processing_errors[:3])}"

        return template('import_transactions_form', message = final_message)
            
    # end csv file import process

    # begin pagination/search of viewing transactions

    @route('/transactions')
    @view('transactions_list')
    def view_transactions():
        description_filter = request.query.get('description','').strip()
        core_account_id_filter = request.query.get('core_account_id','').strip()
        start_date_filter = request.query.get('start_date','').strip()
        end_date_filter = request.query.get('end_date','').strip()

        page = int(request.query.get('page',1))
        per_page = 50

        where_clauses = []
        params = []

        if description_filter:
            where_clauses.append("t.description like ?")
            params.append(f"{description_filter}%")
        if core_account_id_filter:
            where_clauses.append("t.core_account_id = ?")
            params.append(core_account_id_filter)
        if start_date_filter:
            where_clauses.append("t.transaction_date >= ?")
            params.append(start_date_filter)
        if end_date_filter:
            where_clauses.append("t.transaction_date <= ?")
            params.append(end_date_filter)

        where_sql = " and ".join(where_clauses) if where_clauses else "1=1"

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        count_sql = f"select count(*) from transactions t where {where_sql}"
        c.execute(count_sql,params)
        total_records = c.fetchone()[0]
        total_pages = math.ceil(total_records / per_page)

        offset = (page -1) * per_page

        main_sql = f"""
            select t.transaction_id
                  ,t.transaction_date
                  ,t.description
                  ,t.amount
                  ,cat.category_name as category_name
                  ,ca.core_account_name
                  ,t.has_receipt
                  ,t.import_date
                  ,t.last_modified_ts
            from transactions t
            left join categories cat on t.category_id = cat.category_id
            left join core_accounts ca on t.core_account_id = ca.core_account_id
            where {where_sql}
            order by t.transaction_date desc, t.transaction_id desc
            limit ? offset ?
            """
        
        final_params = params + [per_page,offset]
        c.execute(main_sql,final_params)
        transactions_for_page = c.fetchall()

        c.execute("select core_account_id,core_account_name from core_accounts order by core_account_name")
        all_accounts = c.fetchall()

        conn.close()

        return dict(
            transactions = transactions_for_page,
            current_page = page,
            total_pages = total_pages,
            description_filter = description_filter,
            core_account_id_filter = core_account_id_filter,
            start_date_filter = start_date_filter,
            end_date_filter = end_date_filter,
            all_accounts = all_accounts,
            title = "View Transactions"
        )
    
    # end transaction pagination
    
    # begin receipt scan route

    @route('/scan_receipt/<transaction_id:int>', method='GET')
    @view('scan_receipt_form')
    def show_scan_form(transaction_id):
        return dict(transaction_id=transaction_id,
                    title="Scan a New Receipt"
                    )
    
    @route('/scan_receipt/<transaction_id:int>', method='POST')
    def do_scan_receipt(transaction_id):
        upload = request.files.get('receipt_image')
    
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(upload.filename)[1]) as temp_file:
            upload.save(temp_file.name, overwrite=True)
            temp_filepath = temp_file.name
    
        try:
            raw_text = ""
            print(f"Processing file: {temp_filepath}")
    
            if temp_filepath.lower().endswith('.pdf'):
                images = convert_from_path(temp_filepath)
                for img in images:
                    raw_text += pytesseract.image_to_string(img) + "\n\n--- Page Break ---\n\n"
            else:
                img = Image.open(temp_filepath)
                raw_text = pytesseract.image_to_string(img)

            extracted_data = extract_receipt_details(raw_text)

            print("--- RAW OCR TEXT ---")
            print(raw_text)
            print("--- EXTRACTED DATA ---")
            print(extracted_data)

            return template('verify_receipt', extracted = extracted_data,
                                                transaction_id=transaction_id)
                    
        except Exception as e:
            import traceback
            traceback.print_exc()
            return f"An error occurred: {e}"
        finally:
            if os.path.exists(temp_filepath):
                os.remove(temp_filepath)

    @route('/save_scanned_receipt/<transaction_id:int>', method='POST')
    def save_scanned_receipt(transaction_id):
        store = request.forms.get('store').strip()
        total_cost = request.forms.get('cost').strip()
        purchasedate = request.forms.get('purchasedate').strip()
        line_item_json = request.forms.get('line_items_json')
        line_items = json.loads(line_item_json)

        import_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("BEGIN TRANSACTION;")
        try:
            c.execute("""
                INSERT INTO receipt_summaries(transaction_id, store, purchase_date, total_amount, import_date) 
                VALUES (?, ?, ?, ?, ?)""",
                (transaction_id, store, purchasedate, float(total_cost), import_timestamp)
            )
            new_summary_id = c.lastrowid 

            if line_items:
                for item in line_items:
                    c.execute("""
                        INSERT INTO receipt_line_items(summary_id, description, quantity, cost)
                        VALUES (?, ?, ?, ?)""",
                        (new_summary_id, item['description'], item['quantity'], item['cost'])
                    )

            c.execute("update transactions set has_receipt = 1 where transaction_id = ?", (transaction_id,))

            conn.commit()
        except Exception as e:
            conn.rollback() 
            print("ERROR saving scanned receipt:",e)
            raise e
        finally:
            conn.close()

        redirect('/transactions')

    # end receipt scan route

    # begin add_receipt route

    @route('/add_receipt', method='GET')
    @view('new_receipt_manual') 
    def show_manual_add_form():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
    
        c.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
        all_categories = c.fetchall()
        conn.close()
    
        return dict(
        all_categories_json=json.dumps(all_categories),
        title="Add Receipt Manually"
        )

    @route('/add_receipt', method='POST')
    def process_manual_add_form():
        store = request.forms.get('store').strip()
        purchasedate = request.forms.get('purchasedate').strip()
        item_descs = request.forms.getall('item_desc')
        item_category_ids = request.forms.getall('item_category_id')
        item_qtys = request.forms.getall('item_qty')
        item_costs = request.forms.getall('item_cost')

        import_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        total_cost = sum([float(cost) for cost in item_costs])

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        c.execute("""
            INSERT INTO receipt_summaries(store, purchase_date, total_amount, import_date) 
            VALUES (?, ?, ?, ?)""",
            (store, purchasedate, total_cost, import_timestamp)
        )
        new_summary_id = c.lastrowid

        for desc, cat_id, qty, cost in zip(item_descs, item_category_ids, item_qtys, item_costs):
            c.execute("""
                INSERT INTO receipts(summary_id, item, category_id, quantity, cost)
                VALUES (?, ?, ?, ?, ?)""",
                (new_summary_id, desc.strip(), cat_id, int(qty), float(cost))
            )
    
        conn.commit()
        conn.close()
    
        redirect('/list')

    # end add_receipt route

    # begin chart building route

    @route('/api/spending-by-category')
    def api_spending_by_category ():
        today = datetime.now()
        start_of_month = today.strftime('%Y-%m-01')
        end_of_month = today .strftime('%Y-%m-d')

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # query to build report
        c.execute("""
        select 
            category_name
            ,sum(expense_amount) as total_amount
        from (
            select
                cat.category_name as category_name
                ,abs(t.amount) as expense_amount
            from transactions as t
            join categories as cat on t.category_id = cat.category_id
            where t.amount < 0 and t.transaction_date between ? and ?

            union all

            select 
                cat.category_name as category_name
                ,r.cost as expense_amount
            from receipts as r 
            join receipt_summaries as rs on r.summary_id = rs.summary_id
            join categories as cat on r.category_id = cat.category_id
            where rs.purchase_date between ? and ?
        ) as all_expenses
        where category_name is not null
        group by category_name
        order by total_amount desc
        """, (start_of_month,end_of_month,start_of_month,end_of_month))

        results = c.fetchall()
        conn.close()

        labels = [row['category_name'] for row in results]
        data = [row['total_amount'] for row in results]

        response.content_type = 'application/json'
        return json.dumps({'labels': labels, 'data': data})
    
    # end chart report route 

    # begin category report table 

    @route('/reports/spending-by-category')
    @view('reports')
    def show_category_pie_chart():
        return dict(title="Spending by Category Report")

    # end chart building route

    #begin category totals table view report route

    @route('/api/category-totals')
    def api_category_totals():
        today = datetime.now()
        start_of_month = today.strftime('%Y-%m-01')
        end_of_month = today .strftime('%Y-%m-d')

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("""
            SELECT
                category_name,
                SUM(amount) AS net_total
            FROM (
                SELECT
                    cat.category_name AS category_name,
                    t.amount AS amount
                FROM transactions AS t
                LEFT JOIN categories AS cat ON t.category_id = cat.category_id
                WHERE t.transaction_date BETWEEN ? AND ?

                UNION ALL

                SELECT
                    cat.category_name AS category_name,
                    -r.cost AS amount
                FROM receipts AS r
                JOIN receipt_summaries AS rs ON r.summary_id = rs.summary_id
                LEFT JOIN categories AS cat ON r.category_id = cat.category_id
                WHERE rs.purchase_date BETWEEN ? AND ?
            ) AS all_entries
            GROUP BY category_name
            ORDER BY category_name
        """, (start_of_month, end_of_month, start_of_month, end_of_month))

        results = c.fetchall()
        conn.close()

        category_totals = [dict(row) for row in results]

        response.content_type = 'application/json'
        return json.dumps(category_totals)
    
    @route('/reports/category-totals')
    @view('category_totals_report')
    def show_category_totals_report():
        return dict(title="Category Totals Report")
    
    # end category totals report

    # begin show reports page

    @route('/reports')
    @view('reports_index')
    def show_reports_index():
        return dict(title="Available Reports")
    
    # end show reports page

    # begin manage categories

    @route('/manage/categories')
    @view('manage_categories')
    def manage_categories():
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("select category_id,category_name from categories order by category_name")
        all_categories = c.fetchall()
        conn.close()

        return dict(
            categories = all_categories,
            title = "Manage Categories'"
        )
    
    @route('/delete/category/<category_id:int>',method='POST')
    def delete_category(category_id):
        conn = None
        try:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()

            c.execute("BEGIN TRANSACTION;")
            c.execute("update transactions set category_id = NULL where category_id = ?",(category_id,))
            c.execute("update receipts set category_id = NULL where category_id = ?", (category_id,))
            c.execute("delete from categories where category_id = ?", (category_id,))
            conn.commit()

            return json.dumps({'success': True})
        
        except Exception as e:
            if conn:
                conn.rollback()
            import traceback
            traceback.print_exc()
            
            return json.dumps({'success': False, 'message': str(e)})
        finally:
            if conn:
                conn.close()

    @route('/update/category/<category_id:int>',method='POST')
    def update_category(category_id):
        try:
            data = request.json
            new_name = data.get('name').strip()

            if not new_name:
                return json.dumps({'success': False, 'message': 'Category name cannot be empty.'})
            
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("update categories set category_name = ? where category_id = ?", (new_name,category_id))
            conn.commit()
            conn.close()

            return json.dumps({'success': True})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return json.dumps({'success': False, 'message': str(e)})