%# views/reports_index.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year, page_specific_css=['reports-index-style.css'])

<div class= "reports-index">
    <h2>Available Reports</h2>
        <p>Please select a report from the list below.</p>

    <div class="form-row">
        <div class = "form-group">
            <ul class="report-index-list">
                <li><a href="/reports/spending-by-category">Spending by Category (Pie Chart)</a></li>
                <li><a href="/reports/category-totals">Category Totals (Table View)</a></li>
            </ul>
        </div>
    </div>
</div>