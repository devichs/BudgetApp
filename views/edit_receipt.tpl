%# views/edit_receipt.tpl

%# Assuming 'no' is the ID, and 'old_data' is a tuple/list:
%# (store, category, item, quantity, ui, cost, purchasedate, status_if_exists)
% rebase('base.tpl', title='Edit Expense ID: ' + str(no), load_base_style=True, page_specific_css=['edit-receipts-style.css'])
% current_status = old_data[7] if old_data and len(old_data) > 7 else 'open'

<p>Edit the expense with ID = {{no}}</p>

<form action="/edit/{{no}}" method="post">  
    <div>
        <label for="store">Store:</label>
        <input type="text" id="store" name="store" value="{{old_data[0] if old_data and len(old_data) > 0 else ''}}" size="30" maxlength="30">
    </div>
    <div>
        <label for="category">Category:</label>
        <input type="text" id="category" name="category" value="{{old_data[1] if old_data and len(old_data) > 1 else ''}}" size="30" maxlength="30">
    </div>
    <div>
        <label for="item">Item:</label>
        <input type="text" id="item" name="item" value="{{old_data[2] if old_data and len(old_data) > 2 else ''}}" size="30" maxlength="30">
    </div>
    <div>
        <label for="quantity">Quantity:</label>
        <input type="text" id="quantity" name="quantity" value="{{old_data[3] if old_data and len(old_data) > 3 else ''}}" size="30" maxlength="30">
    </div>
    <div>
        <label for="ui">UI (Unit of Issue):</label>
        <input type="text" id="ui" name="ui" value="{{old_data[4] if old_data and len(old_data) > 4 else ''}}" size="2" maxlength="2"> </div>
    <div>
        <label for="cost">Cost:</label>
        <input type="text" id="cost" name="cost" value="{{old_data[5] if old_data and len(old_data) > 5 else ''}}" size="10">
    </div>
    <div>
        <label for="purchasedate">Date (YYYY-MM-DD):</label>
        <input type="text" id="purchasedate" name="purchasedate" value="{{old_data[6] if old_data and len(old_data) > 6 else ''}}" size="10">
    </div>

    %# Status field - check if you have 'status' in your receipts table
    %# If old_data[7] is supposed to be the status:
    %# status_val = old_data[7] if old_data and len(old_data) > 7 else 'open'
    <div>
        <label for="status">Status:</label>
        <select id="status" name="status">
            <option value="open" {{'selected' if current_status == 'open' else ''}}>Open</option>
            <option value="closed" {{'selected' if current_status == 'closed' else ''}}>Closed</option>
        </select>
    </div>
    <br />
    <div>
        <input type="submit" name="save" value="Save Changes">
    </div>
</form>

<p><a href="/list">Back to Expense List</a></p>