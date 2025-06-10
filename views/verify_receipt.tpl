%# views/verify_receipt.tpl
% rebase('base.tpl', title='Verify Scanned Receipt', load_base_style=True, current_year=current_year)

<h2>Verify Scanned Details</h2>
<p>Please review and correct the extracted data, then fill in the remaining fields.</p>

%# This form will submit the data to a new route that saves it.
<form action="/save_scanned_receipt" method="post" class="new-item">
    <ul>
        <li>
            <label for="store">Store</label>
            <input type="text" id="store" name="store" value="{{extracted.get('store_name', '')}}">
        </li>
        <li>
            <label for="purchasedate">Purchase Date (YYYY-MM-DD)</label>
            <input type="date" id="purchasedate" name="purchasedate" value="{{extracted.get('purchase_date', '')}}">
        </li>
         <li>
            <label for="cost">Cost</label>
            <input type="text" id="cost" name="cost" value="{{extracted.get('total_amount', '')}}">
        </li>
        <li>
            <label for="category">Category</label>
            <input type="text" id="category" name="category" placeholder="e.g., Groceries, Restaurants" required>
        </li>
        <li>
            <label for="item">Item(s)</label>
            <input type="text" id="item" name="item" placeholder="e.g., Milk, Bread, Lunch" required>
        </li>
        <li>
            <label for="quantity">Quantity</label>
            <input type="text" id="quantity" name="quantity" value="1">
        </li>
         <li>
            <label for="ui">UI</label>
            <input type="text" id="ui" name="ui" value="EA"> </li>
        <li>
            <input type="submit" value="Save Verified Receipt">
        </li>
    </ul>
</form>