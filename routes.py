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

# function to manage categories
def get_or_create_subcategory_id(main_category_name, sub_category_name, db_cursor):
    main_category_name = main_category_name.strip()
    sub_category_name = sub_category_name.strip()
    
    if not main_category_name or not sub_category_name:
        return None

    db_cursor.execute("SELECT main_category_id FROM main_categories WHERE main_category_name = ?", (main_category_name,))
    main_cat_result = db_cursor.fetchone()
    
    if not main_cat_result:
        print(f"Warning: Main category '{main_category_name}' not found in database.")
        return None 
    main_cat_id = main_cat_result[0]

    db_cursor.execute("""
        SELECT sub_category_id FROM sub_categories 
        WHERE sub_category_name = ? AND main_category_id = ?
    """, (sub_category_name, main_cat_id))
    sub_cat_result = db_cursor.fetchone()

    if sub_cat_result:
        return sub_cat_result[0]
    else:
        db_cursor.execute("""
            INSERT INTO sub_categories (sub_category_name, main_category_id) 
            VALUES (?, ?)
        """, (sub_category_name, main_cat_id))
        print(f"Created new sub-category '{sub_category_name}' under '{main_category_name}'.")
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
   
    @route("/budget")
    @view("budget")
    def  unified_budget_view():
        today = datetime.now()
        default_start = today.replace(day=1).strftime('%Y-%m-%d')
        default_end = today .strftime('%Y-%m-%d')
        start_date = request.query.get('start_date', default_start).strip()
        end_date = request.query.get('end_date', default_end).strip()

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            select sum(amount)
            from transactions
            where amount > 0 and transaction_date >= ? and transaction_date <= ?            
        """, (start_date,end_date))
        total_income_result = c.fetchone() [0]
        total_income = total_income_result if total_income_result is not None else 0.0

        c.execute("""
            select sum(amount)
            from transactions
            where amount < 0 and transaction_date >= ? and transaction_date <= ?
        """,(start_date,end_date))
        transactions_expenses_result = c.fetchone()[0]
        transactions_expenses = transactions_expenses_result if transactions_expenses_result is not None else 0.0

        c.execute("""
            select sum(r.cost)
            from receipt_line_items as r
            join receipt_summaries as rs on r.summary_id = rs.summary_id
            where rs.purchase_date between ? and ?
        """, (start_date,end_date))
        receipts_expenses_result = c.fetchone()[0]
        receipts_expenses = receipts_expenses_result if receipts_expenses_result is not None else 0.0

        total_expenses = abs(transactions_expenses) + receipts_expenses

        conn.close()

        whats_left = total_income - total_expenses

        return dict(
            title = "Budget Summary",
            start_date = start_date,
            end_date = end_date,
            total_income = total_income,
            total_expenses = total_expenses,
            whats_left = whats_left
        )

    @route('/edit/<receipt_id:int>', method='GET')
    @view('edit_receipt') 
    def show_edit_receipt_form(receipt_line_item_id):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            SELECT rs.store
            ,c.category_name
            ,r.description
            ,r.quantity
            ,r.cost
            ,r.purchasedate
            from transactions t
            join receipt_summaries rs on rs.transaction_id = t.transaction_id
            join receipt_line_items r on r.summary_id = rs.summary_id
            join sub_categories c on c.sub_category_id = t.sub_category_id
            where receipt_line_item_id = ?        
        """, (receipt_line_item_id,))
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
        cost = request.forms.get('cost').strip() 
        purchasedate = request.forms.get('purchasedate').strip() 

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
            update receipt_line_items r
            join receipt_summaries rs on r.summary_id = rs.summary_id
            join transactions t on rs.transaction_id = t.transaction_id
            join sub_categories c on c.sub_category_id = t.sub_category_id
            set rs.store = ?
            ,c.sub_dcategory_name = ?
            ,r.description = ?
            ,r.quantity = ?
            ,r.cost = ?
            ,r.purchasedate = ?
            where r.receipt_line_item_id = ?
        """, (store, category, item, quantity, float(cost), purchasedate))
        conn.commit()
        c.close()
        conn.close()

        from bottle import redirect 
        redirect('/list')     

    @route('/import_transactions', method='GET')
    @view('import_transactions_form')
    def show_import_form():
        return dict()
    
    # begin csv file import process

    def get_or_create_categories_id(category_name,db_cursor):
        category_name = category_name.strip()
        if not category_name:
            return None
        db_cursor.execute("select sub_category_id from sub_categories where sub_category_name = ?",(category_name,))
        row = db_cursor.fetchone()
        if row:
            return row[0]
        else:
            db_cursor.execute("insert into sub_categories (sub_category_name) values (?)",(category_name,))
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
        print("\nDEBUG: 1. Starting 'do_import_transactions'.")
        upload = request.files.get('csvfile')
        account_name = request.forms.get('core_account_name')
        account_type = request.forms.get('core_account_type')

        if not upload or not upload.filename.lower().endswith('.csv'):
            return template('import_transactions_form', error_message="You must upload a valid .csv file.")
        if not account_name or not account_name.strip():
            return template('import_transactions_form', error_message="The 'Import From Account' name is required.")

        print("\nDEBUG: 2. Form and file validation passed'.")

        try:
            csv_content = upload.file.read().decode('utf-8')
            stream = io.StringIO(csv_content)
            reader = csv.DictReader(stream)
            print(f"DEBUG: 3. CSV headers found: {reader.fieldnames}")
        except Exception as e:
            print("\nDEBUG: Exiting - Error reading or decoding file: {e}")
            return template('import_transactions_form', error_message=f"Error reading or decoding file: {e}")

        import_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()

        core_account_id = get_or_create_core_account_id(account_name, account_type, c)
        print(f"DEBUG: 4. Got/Created Core Account ID: {core_account_id}")

        transactions_to_add = []
        skipped_count = 0
        imported_count = 0
        processing_errors = []

        print("DEBUG: 5. Starting to loop through CSV rows...")
        row_count = 0
        for row_number, row in enumerate(reader, start=2):
            row_count+= 1
            try:
                date_str = row.get("Date", "").strip()
                description = row.get("Description", "").strip()
                main_category_name = row.get("Category", "").strip()
                sub_category_name = row.get("SubCategory", "").strip()
                amount_str = row.get("Amount", "").strip()

                if not all([date_str, description, amount_str]):
                    print(f"DEBUG: Row {row_number} failed validation: Missing data.")
                    processing_errors.append(f"Row {row_number}: Missing Date, Description, or Amount."); skipped_count += 1; continue
            
                try:
                    datetime.strptime(date_str, '%Y-%m-%d'); transaction_date = date_str
                except ValueError:
                    processing_errors.append(f"Row {row_number}: Invalid date '{date_str}'."); skipped_count += 1; continue
                try:
                    cleaned_amount_str = amount_str.replace(',', ''); amount = float(cleaned_amount_str)
                except ValueError:
                    processing_errors.append(f"Row {row_number}: Invalid amount '{amount_str}'."); skipped_count += 1; continue
            
                sub_category_id = get_or_create_subcategory_id(main_category_name, sub_category_name, c)

                c.execute("SELECT 1 FROM transactions WHERE transaction_date=? AND description=? AND amount=?", (transaction_date, description, amount))
                if c.fetchone():
                    skipped_count += 1; 
                    continue

                transactions_to_add.append({
                    "date": transaction_date, "description": description, "amount": amount,
                    "sub_category_id": sub_category_id,
                    "core_account_id": core_account_id,
                    "notes": "Imported", "import_date": import_timestamp
                })
            
            except Exception as e:
                processing_errors.append(f"Row {row_number}: Unexpected error - {e}"); skipped_count += 1; 
                continue

        print(f"DEBUG: 6. Finished loop. Processed {row_count} rows.")
        #print(f"DEGUG: {date_str} {description} {main_category_name} {sub_category_name } {amount}")  

        if transactions_to_add:
            print(f"DEBUG: 7. Preparing to insert {len(transactions_to_add)} new transactions.")
            sql = "INSERT INTO transactions (transaction_date, description, amount, sub_category_id, core_account_id, notes, import_date) VALUES (?, ?, ?, ?, ?, ?, ?)"
            insert_data = [(tx['date'], tx['description'], tx['amount'], tx['sub_category_id'], tx['core_account_id'], tx['notes'], tx['import_date']) for tx in transactions_to_add]
            c.executemany(sql, insert_data)
            imported_count = len(transactions_to_add)
            print(f"DEBUG: After transactions_to_add - Inserted {len(transactions_to_add)} new transactions.")

        conn.commit()
        conn.close()
        print("DEBUG: 8. Database commit and close successful.")


        final_message = f"Import complete! Successfully imported {imported_count} new transactions."
        if skipped_count > 0: 
            final_message += f" Skipped {skipped_count} existing or invalid rows."
        if processing_errors: 
            final_message += f" Errors encountered: {'; '.join(processing_errors[:3])}"

        print("DEBUG: 9. Rendering final template.")
        return template('import_transactions_form', message=final_message)
            
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
                  ,cat.sub_category_name as category_name
                  ,ca.core_account_name
                  ,t.has_receipt
                  ,t.import_date
                  ,t.last_modified_ts
            from transactions t
            left join sub_categories cat on t.sub_category_id = cat.sub_category_id
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
    
        c.execute("SELECT sub_category_id, sub_category_name FROM sub_categories ORDER BY sub_category_name")
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
        start_date = today.strftime('%Y-%m-%d')
        end_date = today .strftime('%Y-%m-%d')

        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # query to build report
        c.execute("""
        select 
            sub_category_name
            ,sum(expense_amount) as total_amount
        from (
            select
                cat.sub_category_name as category_name
                ,abs(t.amount) as expense_amount
            from transactions as t
            join sub_categories as cat on t.sub_category_id = cat.sub_category_id
            where t.amount < 0 and t.transaction_date between ? and ?

            union all

            select 
                cat.sub_category_name as category_name
                ,r.cost as expense_amount
            from receipts as r 
            join receipt_summaries as rs on r.summary_id = rs.summary_id
            join sub_categories as cat on r.sub_category_id = cat.sub_category_id
            where rs.purchase_date between ? and ?
        ) as all_expenses
        where category_name is not null
        group by category_name
        order by total_amount desc
        """, (start_date,end_date,start_date,end_date))

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
        start_date = today.strftime('%Y-%m-%d')
        end_date = today .strftime('%Y-%m-%d')

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
                LEFT JOIN sub_categories AS cat ON t.sub_category_id = cat.sub_category_id
                WHERE t.transaction_date BETWEEN ? AND ?

                UNION ALL

                SELECT
                    cat.category_name AS category_name,
                    -r.cost AS amount
                FROM receipts AS r
                JOIN receipt_summaries AS rs ON r.summary_id = rs.summary_id
                LEFT JOIN sub_categories AS cat ON r.sub_category_id = cat.sub_category_id
                WHERE rs.purchase_date BETWEEN ? AND ?
            ) AS all_entries
            GROUP BY sub_category_name
            ORDER BY sub_category_name
        """, (start_date, end_date, start_date, end_date))

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
        c.execute("select sub_category_id,sub_category_name from sub_categories order by sub_category_name")
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
            c.execute("update transactions set sub_category_id = NULL where sub_category_id = ?",(category_id,))
            c.execute("update receipt_line_items set sub_category_id = NULL where sub_category_id = ?", (category_id,))
            c.execute("delete from sub_categories where sub_category_id = ?", (category_id,))
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
            c.execute("update sub_categories set sub_category_name = ? where category_id = ?", (new_name,category_id))
            conn.commit()
            conn.close()

            return json.dumps({'success': True})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return json.dumps({'success': False, 'message': str(e)})
        
        # end manage categories 

        #begin line item receipts view

    @route('/view_receipt/<transaction_id:int>')
    @view('view_receipt_details') # We will create this new template
    def view_receipt(transaction_id):
        conn = sqlite3.connect(DB_NAME)
    
        conn.row_factory = sqlite3.Row 
        c = conn.cursor()

        c.execute("""
            SELECT summary_id, store, purchase_date, total_amount 
            FROM receipt_summaries 
            WHERE transaction_id = ?
        """, (transaction_id,))
        summary = c.fetchone()

        line_items = []
        if summary:
            c.execute("""
                SELECT description, quantity, cost 
                FROM receipt_line_items 
                WHERE summary_id = ?
            """, (summary['summary_id'],))
            line_items = c.fetchall()
    
        conn.close()

        return dict(
            summary=summary,
            line_items=line_items,
            transaction_id=transaction_id,
            title="View Receipt Details"
        )

    @route('/manage/descriptions')
    @view('manage_descriptions') # We will create this new template
    def manage_descriptions():
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

    # Query 1: Get all unique descriptions and their most recently assigned category details.
    # This is a complex query that uses a subquery with row_number() to find the latest
    # transaction for each description and then joins to get the category names.
        c.execute("""
            WITH LatestTransactions AS (
                SELECT
                    t.description,
                    t.sub_category_id,
                    ROW_NUMBER() OVER(PARTITION BY t.description ORDER BY t.transaction_date DESC, t.transaction_id DESC) as rn
                FROM transactions t
            )
            SELECT
                lt.description,
                sc.sub_category_id,
                sc.sub_category_name,
                mc.main_category_id,
                mc.main_category_name
            FROM LatestTransactions lt
            LEFT JOIN sub_categories sc ON lt.sub_category_id = sc.sub_category_id
            LEFT JOIN main_categories mc ON sc.main_category_id = mc.main_category_id
            WHERE lt.rn = 1
            ORDER BY lt.description
        """)
        description_data = [dict(row) for row in c.fetchall()]

    # Query 2: Get all main categories for the dropdown
        c.execute("SELECT main_category_id, main_category_name FROM main_categories ORDER BY main_category_name")
        all_main_categories = [dict(row) for row in c.fetchall()]

    # Query 3: Get all sub-categories for the dropdowns
        c.execute("SELECT sub_category_id, sub_category_name, main_category_id FROM sub_categories ORDER BY sub_category_name")
        all_sub_categories = [dict(row) for row in c.fetchall()]

        conn.close()

        return dict(
            description_data=description_data,
            all_main_categories=all_main_categories,
            all_sub_categories_json=json.dumps(all_sub_categories),
            title="Manage Transaction Descriptions"
        )
    
    # In routes.py

    @route('/update/description_category', method='POST')
    def update_description_category():
        description = request.forms.get('description')
        new_sub_category_id = request.forms.get('sub_category_id')

        if not description or not new_sub_category_id:
        # We can add a more user-friendly error page later
            return "Error: Missing description or new sub-category selection."

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
    # This is the powerful bulk update
        c.execute(
            "UPDATE transactions SET sub_category_id = ? WHERE description = ?",
            (new_sub_category_id, description)
        )
        conn.commit()
        conn.close()

    # Redirect back to the management page to see the changes
        redirect('/manage/descriptions')