%# views/view_receipt_details.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<div class="report-container">
    % if summary:
        <h2>Receipt Details for Store: {{summary['store']}}</h2>
        
        <fieldset>
            <legend>Summary</legend>
            <div class="summary-details">
                <p><strong>Purchase Date:</strong> {{summary['purchase_date']}}</p>
                <p><strong>Total Amount:</strong> ${{ "{:,.2f}".format(summary['total_amount']) }}</p>
            </div>
        </fieldset>

        <fieldset>
            <legend>Line Items</legend>
            <table style="width:100%; text-align: left;">
                <thead>
                    <tr>
                        <th>Description</th>
                        <th style="text-align: center;">Quantity</th>
                        <th class="money">Cost</th>
                    </tr>
                </thead>
                <tbody>
                    % for item in line_items:
                    <tr>
                        <td>{{item['description']}}</td>
                        <td style="text-align: center;">{{item['quantity']}}</td>
                        <td class="money">${{ "{:,.2f}".format(item['cost']) }}</td>
                    </tr>
                    % end
                </tbody>
            </table>
        </fieldset>
    % else:
        <h2>No Receipt Found</h2>
        <p>There is no receipt attached to transaction #{{transaction_id}}.</p>
        <p><a href="/scan_receipt/{{transaction_id}}">Would you like to add one now?</a></p>
    % end

    <br>
    <a href="/transactions">Back to Transactions List</a>
</div>

<style>
    .report-container { max-width: 800px; margin: 20px auto; }
    fieldset {
        border: 1px solid #ddd;
        padding: 15px;
        margin-bottom: 20px;
        border-radius: 5px;
    }
    legend {
        font-weight: bold;
        font-size: 1.2em;
        padding: 0 10px;
    }
    .summary-details p {
        margin: 5px 0;
    }
</style>