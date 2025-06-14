%# views/reports_index.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<h2>Available Reports</h2>

<p>Please select a report from the list below.</p>

<ul class="report-list">
    <li><a href="/reports/spending-by-category">Spending by Category (Pie Chart)</a></li>
    <li><a href="/reports/category-totals">Category Totals (Table View)</a></li>
    </ul>

<style>
    .report-list li {
        width: 400px; /* Example styling */
    }
    .report-list a {
        display: block;
        padding: 15px;
        text-decoration: none;
    }
</style>