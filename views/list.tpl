<!DOCTYPE html>
<html>
	<head>
		<title>Receipts</title>
		<link rel = "stylesheet" href = "static\content\list-style.css">
		<script src="static\scripts\sorttable.js"></script>
	</head>
		<body>
			<div class = "nav"><!--navigation menu-->
				<ul class = "nav">
					<li><a href = "http://localhost:5555/new">New Expense</a></li>
					<li><a href = "http://localhost:5555/budget">Budget</a></li>
					<li><a href = "http://localhost:5555/">Home</a></li>
					<li><a href = "http://localhost:5555/list">Import Expense List</a></li>
				</ul>
			</div><!--end navigation menu-->
					<table class = "sortable centered">
					<caption>Current list of items purchased</caption>
						<th>ID</th>
						<th>Store</th>
						<th>Category</th>
						<th>Item</th>
						<th>Quantity</th>
						<th>UI</th>
						<th>Cost</th>
						<th>Purchase date</th>
							%for row in rows:
								<tr>
									%for col in row:
										<td>{{col}}</td>
									%end
								</tr>
							%end
					</table>
		</body>
</html>