%# views/verify_receipt.tpl
% rebase('base.tpl', title='Verify Scanned Receipt', load_base_style=True, current_year=current_year)

%# Import json to pass the list of items to the next step
% import json

<h2>Verify Scanned Details</h2>
<p>Please review and correct the extracted data, then fill in the remaining fields.</p>

% if extracted.get('line_items'):
<fieldset>
    <legend>Extracted Line Items</legend>
    <table style="width:100%; text-align: left;">
        <thead><tr><th>Qty</th><th>Description</th><th style="text-align: right;">Cost</th></tr></thead>
        <tbody>
            % for item in extracted['line_items']:
            <tr>
                <td>{{item['quantity']}}</td>
                <td>{{item['description']}}</td>
                <td style="text-align: right;">${{item['cost']}}</td>
            </tr>
            % end
        </tbody>
    </table>
</fieldset>
% end

<form action="/save_scanned_receipt" method="post" class="new-item">
    <input type="hidden" name="line_items_json" value="{{json.dumps(extracted.get('line_items', []))}}">

    <ul>
        <li><label for="store">Store</label><input type="text" id="store" name="store" value="{{extracted.get('store_name', '')}}"></li>
        <li><label for="purchasedate">Purchase Date (YYYY-MM-DD)</label><input type="date" id="purchasedate" name="purchasedate" value="{{extracted.get('purchase_date', '')}}"></li>
        <li><label for="cost">Total Cost</label><input type="text" id="cost" name="cost" value="{{extracted.get('total_amount', '')}}"></li>
        <li><input type="submit" value="Save Verified Receipt"></li>
    </ul>
</form>