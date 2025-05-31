<!doctype html>
<html class="no-js" lang="{{ locals().get('lang', 'en') }}">
	<head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>{{ title or "What's Left!" }}</title>
        <meta name="description" content="{{ locals().get('description', 'Budget Application') }}">
        <meta name="viewport" content="width=device-width, initial-scale=1">

        <link rel="stylesheet" href="/static/content/budget-style.css"> % if defined('page_specific_css'):
            % for css_file in page_specific_css:
        <link rel="stylesheet" href="/static/content/{{css_file}}">
            % end
        % end

    </head>
		<body>
			<header class="site-header">
				<div class="container">
					<h1><a href="/home">What's Left!</a></h1>
					<nav>
						<a href="/home">Home</a>
						<a href="/budget">Budget</a>
						<a href="/list">Expenses</a>
						<a href="/new">Add Expense</a>
						<a href="/newbudget">Set Budget</a>
						<a href="/import_transactions">Import</a>
					</nav>
				</div>
			</header>
	
			<main class="site-content">
				<div class="container">
					% include # This is where the content of the child template (that called rebase) will be inserted.
				</div>
			</main>
	
			<footer class="site-footer">
				<div class="container">
					<p>&copy; {{ locals().get('current_year', '2025') }} Your Budget App</p>
				</div>
			</footer>
	
			<script src="/static/scripts/sorttable.js"></script>
		</body>
</html>