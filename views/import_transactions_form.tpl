%# views/import_transactions_form.tpl
% rebase('base.tpl', title='Import Transactions - What\'s Left!', load_base_style=True, current_year=current_year, page_specific_css=['import-transactions-style.css'])

<div class="import-transactions">
    <h2>Import Transactions from a Core Account</h2>

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

	<form action="/import_transactions" method="post" enctype="multipart/form-data" class="filter-form">
		<div class="form-row">
			<div class="form-group">
				<label for="core_account_name">Import From Core Account:</label>
				<input type="text" id="core_account_name" name="core_account_name" placeholder="e.g., Amex Gold Card" required>
			</div>
		</div>
		<br>
		<div class="form-row">
			<div class="form-group">
			    <label for="core_account_type">Account Type (Optional):</label>
			    <input type="text" id="core_account_type" name="core_account_type" placeholder="e.g., Credit Card, Checking">
            </div>
        </div>
		<br>
		<div class="form-row">
			<div class="form-group">
			    <label for="csvfile">Select CSV file to import:</label>
			    <p style="font-size: smaller; color: #555;">File must have columns: "Date", "Description", "Category", "SubCategory", "Amount"</p>
			    <input type="file" id="csvfile" name="csvfile" accept=".csv" required>
            </div>
        </div>
		<br>
		<div class="form-row">
			<div class="form-group">
			    <input type="submit" value="Import Transactions">
            </div>
        </div>
	</form>
</div>