%# views/new_receipt_manual.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<h2>Add a New Receipt Manually</h2>

<form action="/add_receipt" method="post" class="filter-form">
    <fieldset>
        <legend>Receipt Summary</legend>
        <div class="form-row">
            <div class="form-group">
                <label for="store">Store</label>
                <input type="text" id="store" name="store" required>
            </div>
            <div class="form-group">
                <label for="purchasedate">Purchase Date</label>
                <input type="date" id="purchasedate" name="purchasedate" required>
            </div>
        </div>
    </fieldset>

    <fieldset>
        <legend>Line Items</legend>
        <table id="line-items-table" style="width: 100%;">
            <thead>
                <tr>
                    <th>Item Description</th>
                    <th>Category</th>
                    <th>Quantity</th>
                    <th>Cost</th>
                    <th></th> </tr>
            </thead>
            <tbody id="line-items-body">
                </tbody>
        </table>
        <br>
        <button type="button" onclick="addLineItem()">+ Add Item</button>
    </fieldset>

    <br>
    <div class="form-row">
        <button type="submit">Save Entire Receipt</button>
    </div>
</form>

<script>
    // Get the categories data passed from our Python route
    const categories = {{!all_categories_json}}; // Using ! to output raw data

    function addLineItem() {
        const tbody = document.getElementById('line-items-body');
        const newRow = tbody.insertRow();

        // Create cells for the new row
        const cellDesc = newRow.insertCell();
        const cellCat = newRow.insertCell();
        const cellQty = newRow.insertCell();
        const cellCost = newRow.insertCell();
        const cellRemove = newRow.insertCell();

        // Add inputs to each cell
        cellDesc.innerHTML = '<input type="text" name="item_desc" required>';
        
        // Create the category dropdown
        let categorySelect = '<select name="item_category_id" required><option value="">--Select--</option>';
        for (const category of categories) {
            categorySelect += `<option value="${category[0]}">${category[1]}</option>`;
        }
        categorySelect += '</select>';
        cellCat.innerHTML = categorySelect;

        cellQty.innerHTML = '<input type="number" name="item_qty" value="1" style="width: 60px;" required>';
        cellCost.innerHTML = '<input type="number" step="0.01" name="item_cost" placeholder="0.00" style="width: 100px;" required>';
        cellRemove.innerHTML = '<button type="button" onclick="removeLineItem(this)">Remove</button>';
    }

    function removeLineItem(button) {
        // Get the row (which is the button's parent's parent) and remove it
        const row = button.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }

    // Add one line automatically when the page loads
    window.onload = function() {
        addLineItem();
    };
</script>