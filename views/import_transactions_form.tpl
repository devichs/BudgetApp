%# views/import_transactions_form.tpl
% rebase('base.tpl', title='Import Transactions - What\'s Left!', load_base_style=True, current_year=current_year, page_specific_css=['import-transactions-style.css'])

<ul class = "ulmainmenu">
	<li class = "limainmenu"><a class = "amenu" href = "/budget">Go To Budget</a></li>
	<li class = "limainmenu"><a class = "amenu" href = "/list">View Expense List</a></li>
	<li class = "limainmenu"><a class = "amenu" href = "/import_transactions">Cancel Import Transactions</a></li>	
	<li class = "limainmenu"><a class = "amenu" href = "http://localhost:5555/">Home</a></li>	
</ul>

<fieldset>
    <legend>Import Transactions from a Core Account CSV export file</legend>

% if defined('message') and message:
<div class="message-box success">
    <strong>Success!</strong><br>
    {{message}}
</div>
% end
% if defined('error_message') and error_message:
<div class="message-box error">
    <strong>Error:</strong><br>
    {{error_message}}
</div>
% end

<form action="/import_transactions" method="post" enctype="multipart/form-data">
    <div>
        <label for="core_account_name">Import From Account:</label>
        <input type="text" id="core_account_name" name="core_account_name" placeholder="e.g., Amex Gold Card" required>
    </div>
    <br>
    <div>
        <label for="core_account_type">Account Type (Optional):</label>
        <input type="text" id="core_account_type" name="core_account_type" placeholder="e.g., Credit Card, Checking">
    </div>
    <br>
    <div>
        <label for="csvfile">Select CSV file to import:</label>
        <p style="font-size: smaller; color: #555;">File must have columns: "Date", "Description", "Category", "SubCategory", "Amount"</p>
        <input type="file" id="csvfile" name="csvfile" accept=".csv" required>
    </div>
    <br>
    <div>
        <input type="submit" value="Import Transactions">
    </div>
</form>