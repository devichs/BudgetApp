%# views/index.tpl
% rebase('base.tpl', title='Home Page', current_year=current_year, page_specific_css=['index-style.css'])
%# The 'current_year' and 'datetime' would need to be passed from your Python route
%# Or, if index-style.css is meant to be global, move it to base.tpl

<p>Welcome to your Budget Application! This is the unique content for the home page.</p>
<p>Here are your options:</p>
<ul>
    <li><a href="/budget">View Budget</a></li>
    <li><a href="/newbudget">Update Budget</a></li>
    <li><a href="/list">View Expense List</a></li>
    <li><a href="/new">Add New Expense</a></li>
    <li><a href="/import_transactions">Import Transactions from CSV</a></li>
</ul>