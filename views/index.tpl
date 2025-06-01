%# views/index.tpl
% rebase('base.tpl', title='Home - What\'s Left!', current_year=current_year, page_specific_css=['index-style.css'])

<nav class="page-navigation">
    <ul>
        <li><a href="/budget">View Budget</a></li>
        <li><a href="/newbudget">Update Budget</a></li>
        <li><a href="/list">View Expense List</a></li>
        <li><a href="/new">Add New Expense</a></li>
        <li><a href="/import_transactions">Import Transactions from CSV</a></li>
    </ul>
</nav>