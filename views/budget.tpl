<!DOCTYPE html>
<html>
	<head>
		<title>Receipts - Budget</title>
		<link rel = "stylesheet" href = "static\content\budget-style.css">
		<script src="static\scripts\sorttable.js"></script>
	</head>
		<body>
			<ul>
				<li><a href = "http://localhost:5555/newbudget">Update Budget</a></li>
				<li><a href = "http://localhost:5555/list">Expense List</a></li>
				<li><a href = "http://localhost:5555/">Home</a></li>
			</ul>
				<table class = "sortable centered budget">
				<caption>Budget</caption>
					<th>amount</th>
					<th>date set</th>
					<th>expense total</th>
					<th>whats left</th>
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