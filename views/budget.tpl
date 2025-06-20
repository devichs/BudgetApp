%# views/budget.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<div class="budget-summary">
    <h2>Budget Summary</h2>
    
    <form action="/budget" method="get" class="filter-form">
        <div class="form-row">
            <div class="form-group">
                <label for="start_date">Start Date:</label>
                <input type="date" id="start_date" name="start_date" value="{{start_date}}">
            </div>
            <div class="form-group">
                <label for="end_date">End Date:</label>
                <input type="date" id="end_date" name="end_date" value="{{end_date}}">
            </div>
        </div>
        <div class="form-row">
            <button type="submit">Update View</button>
        </div>
    </form>
    
    <hr style="margin: 20px 0;">

    <div class="summary-item">
        <span class="label">Total Income:</span>
        <span class="value income">${{ "{:,.2f}".format(total_income) }}</span>
    </div>

    <div class="summary-item">
        <span class="label">Total Expenses:</span>
        <span class="value expenses">-${{ "{:,.2f}".format(total_expenses) }}</span>
    </div>
    
    <div class="summary-item">
        <span class="label">What's Left:</span>
        <span class="value balance">${{ "{:,.2f}".format(whats_left) }}</span>
    </div>
</div>


<style>
/* You can reuse these styles or move them to a global css file */
.budget-summary { max-width: 600px; margin: 20px auto; padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 8px; text-align: center; }
.budget-summary h2 { margin-top: 0; }
.summary-item { display: flex; justify-content: space-between; padding: 15px 10px; border-bottom: 1px solid #eee; font-size: 1.2em; }
.summary-item:last-child { border-bottom: none; }
.summary-item .label { font-weight: bold; }
.summary-item .value { font-family: monospace; }
.income { color: #28a745; }
.expenses { color: #dc3545; }
.balance { font-weight: bold; font-size: 1.4em; }

/* Styles for the filter form */
.filter-form { border: 1px solid #ddd; padding: 15px; margin-top: 20px; border-radius: 5px; }
.filter-form .form-row { display: flex; gap: 20px; margin-bottom: 10px; justify-content: center; align-items: center; }
.filter-form .form-group { flex: 1; }
.filter-form label { display: block; margin-bottom: 5px; font-size: 14px; text-align: left;}
.filter-form input, .filter-form button { width: 100%; padding: 8px; box-sizing: border-box; }
</style>