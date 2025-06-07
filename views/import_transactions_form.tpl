%# views/import_transactions_form.tpl
% rebase('base.tpl', title='Import Transactions - What\'s Left!', load_base_style=True, current_year=current_year)

<h2>Import Transactions from CSV</h2>

% if defined('message') and message:
    <p style="color: green; border: 1px solid green; padding: 10px; border-radius: 5px;">{{message}}</p>
% end
% if defined('error_message') and error_message:
    <p style="color: red; border: 1px solid red; padding: 10px; border-radius: 5px;">{{error_message}}</p>
% end

<form action="/import_transactions" method="post" enctype="multipart/form-data">
    <div>
        <label for="csvfile">Select CSV file to import:</label>
        <p style="font-size: smaller; color: #555;">File must have columns: "Date", "Description", "Category", "Amount"</p>
        <input type="file" id="csvfile" name="csvfile" accept=".csv" required>
    </div>
    <br>
    <div>
        <input type="submit" value="Import Transactions">
    </div>
</form>