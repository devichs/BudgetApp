<!doctype html>
<html class="no-js" lang="{{ locals().get('lang', 'en') }}">
	<head>
        <meta charset="utf-8">
        <meta http-equiv="x-ua-compatible" content="ie=edge">
        <title>{{ title or "What's Left!" }}</title>
        <meta name="description" content="{{ locals().get('description', 'Budget Application') }}">
        <meta name="viewport" content="width=device-width, initial-scale=1">

		% if load_base_style:
        <link rel="stylesheet" href="/static/content/base-style.css">
		% end

		% if defined('page_specific_css') and page_specific_css:
            % for css_file in page_specific_css:
        <link rel="stylesheet" href="/static/content/{{css_file.strip()}}">
            % end
        % end

    </head>
		<body>
			<header class="site-header">
				<div class="container">
					<h1><a href="/home">What's Left!</a></h1>
				</div>
			</header>
				<main class="site-content">
					<div class="container">
						% include # content of the child template inserted here.
					</div>
				</main>
				
			<footer class="site-footer">
				<div class="container">
					<p>&copy; {{ locals().get('current_year', '2025') }} What's Left!</p>
				</div>
			</footer>
	
			<script src="/static/scripts/sorttable.js"></script>
		</body>
</html>