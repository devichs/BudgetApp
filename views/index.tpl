%# views/index.tpl
% rebase('base.tpl', title='Home - What\'s Left!', load_base_style=True, current_year=current_year, page_specific_css=['index-style.css'])

<nav class="page-navigation">
    <ul>
        <li><a href="/budget">View Budget</a></li>
        <li><a href="/transactions">View Transactions</a></li>
        <li><a href="/import_transactions">Import Transactions</a></li>
        <li><a href="/reports">View Reports</a></li>
        <li><a href="/manage/categories">Manage Categories</a></li>
        <li><a href="/manage/descriptions">Manage Descriptions</a></li>
    </ul>
</nav>