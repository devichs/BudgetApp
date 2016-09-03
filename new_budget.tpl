<!DOCTYPE html>
<html>
	<head>
		<title>Receipts - Budget</title>
		<link rel = "stylesheet" href = "update-budget-style.css">
		<script src="sorttable.js"></script>
	</head>
		<body>
			<ul class = "ulmenu">
				<li class = "limenu"><a class = "amenu" href = "http://localhost:8080/budget">Budget</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:8080/index">Home</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:8080/budget">Cancel</a></li>
			</ul>
				<fieldset>
					<legend>Update Budget Amount:</legend>			
						<form class = "update-budget" action="/newbudget" method="GET">
							<ul>
							<li>
								<label for="amount">Budget Amount</label>
								<input type="text" name="amount" required = "required"/>
								<span>Enter Your Budget for the Month</span>
							</li>
							<li>
							<input type="submit" name="update" value="Update"/>
							<input type="reset" name="reset" value="Reset"/>
							</ul>
						</form>
					</legend>
				</fieldset>
		</body>
</html>