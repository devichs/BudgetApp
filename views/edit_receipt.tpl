%# views/edit_receipt.tpl

%# Assuming 'no' is the ID, and 'old_data' is a tuple/list:
%# (store, category, item, quantity, ui, cost, purchasedate, status_if_exists)
% rebase('base.tpl', title='Edit Expense ID: ' + str(no), load_base_style=True, page_specific_css=['edit-receipts-style.css'])
% current_status = old_data[7] if old_data and len(old_data) > 7 else 'open'

<ul class = "ulmainmenu">
	<li class = "limainmenu"><a class = "amenu" href = "/budget">Go To Budget</a></li>
	<li class = "limainmenu"><a class = "amenu" href = "/list">View Expense List</a></li>
	<li class = "limainmenu"><a class = "amenu" href = "/list">Cancel Edit Expense</a></li>	
	<li class = "limainmenu"><a class = "amenu" href = "http://localhost:5555/">Home</a></li>	
</ul>

<fieldset>
    <legend>Edit the expense with ID = {{no}}</legend>

<form class = "edit-receipt" action="/edit/{{no}}" method="post">
    <ul class = "uledititemmenu">
        <li>
            <label for="store">Store:</label>
            <input type="text" id="store" name="store" value="{{old_data[0] if old_data and len(old_data) > 0 else ''}}" size="30" maxlength="30">
            <span>Enter changes to the Store</span>
        </li>
        <li>
            <label for="category">Category:</label>
            <input type="text" id="category" name="category" value="{{old_data[1] if old_data and len(old_data) > 1 else ''}}" size="30" maxlength="30">
            <span>Enter changes to the Category</span>
        <li>
            <label for="item">Item:</label>
            <input type="text" id="item" name="item" value="{{old_data[2] if old_data and len(old_data) > 2 else ''}}" size="30" maxlength="30">
            <span>Enter changes to the Item</span>
        </li>
        <li>
            <label for="quantity">Quantity:</label>
            <input type="text" id="quantity" name="quantity" value="{{old_data[3] if old_data and len(old_data) > 3 else ''}}" size="30" maxlength="30">
            <span>Enter changes to the Quantity</span>
        </li>
        <li>
            <label for="ui">UI (Unit of Issue):</label>
            <input type="text" id="ui" name="ui" value="{{old_data[4] if old_data and len(old_data) > 4 else ''}}" size="2" maxlength="2"> 
            <span>Enter changes to the Unit of Issue</span>
        </li>
        <li>
            <label for="cost">Cost:</label>
            <input type="text" id="cost" name="cost" value="{{old_data[5] if old_data and len(old_data) > 5 else ''}}" size="10">
            <span>Enter changes to the Cost</span>
        </li>
        <li>
            <label for="purchasedate">Purchase Date (format) (YYYY-MM-DD):</label>
            <input type="date" id="purchasedate" name="purchasedate" value="{{old_data[6] if old_data and len(old_data) > 6 else ''}}" size="10">
            <span>Enter changes to the Purchase Date</span>
        </li>


    %# Status field - check if you have 'status' in your receipts table
    %# If old_data[7] is supposed to be the status:
    %# status_val = old_data[7] if old_data and len(old_data) > 7 else 'open'
        <li>
            <label for="status">Status:</label>
            <select id="status" name="status">
                <option value="open" {{'selected' if current_status == 'open' else ''}}>Open</option>
                <option value="closed" {{'selected' if current_status == 'closed' else ''}}>Closed</option>
            </select>
        </li>
    </ul>

    <br />
    
        <input type="submit" name="save" value="Save Changes">
        <input type="reset" name="reset" value="Reset"/>
</fieldset>   
</form>
