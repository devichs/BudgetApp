%# views/budget.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<style>
    .budget-summary {
        max-width: 600px;
        margin: 20px auto;
        padding: 20px;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        border-radius: 8px;
        text-align: center;
    }
    .budget-summary h2 {
        margin-top: 0;
    }
    .summary-item {
        display: flex;
        justify-content: space-between;
        padding: 15px 10px;
        border-bottom: 1px solid #eee;
        font-size: 1.2em;
    }
    .summary-item:last-child {
        border-bottom: none;
    }
    .summary-item .label {
        font-weight: bold;
    }
    .summary-item .value {
        font-family: monospace;
    }
    .income { color: #28a745; }
    .expenses { color: #dc3545; }
    .balance { font-weight: bold; font-size: 1.4em; }
</style>

<div class="budget-summary">
    <h2>Budget Summary</h2>
    <p>Showing figures for the period: {{start_date}} to {{end_date}}</p>

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