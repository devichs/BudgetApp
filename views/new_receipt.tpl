<!DOCTYPE html>
<html>
	<head>
		<title>Receipts</title>
		<link rel = "stylesheet" href = "static\content\new-style.css">
		<script src="static\scripts\sorttable.js"></script>
		<script type="text/javascript">
		//auto expand textarea
		function adjust_textarea(h) {
			h.style.height = "20px";
			h.style.height = (h.scrollHeight)+"px";
		}
		</script>
	</head>
		<body>
			<ul class = "ulmenu">
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/budget">Budget</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/list">Expense List</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/">Home</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/budget">Cancel</a></li>		
			</ul>
				<fieldset>
					<legend>Add a new item to the list:</legend>
						<form class =  "new-item" action="/new" method="GET">
							<ul>
							<li>
								<label for="store">Store</label>
								<input type="text" maxlength="30" name="store" required = "required"/>
								<span>Enter the name of the Store here</span>
							</li>
							<li>
								<label for="category">Category</label>
								<input type="text" maxlength="30" name="category" required = "required"/>
								<span>Enter the item Category here</span>
							</li>
							<li>
								<label for="item">Item</label>
								<input type="text" maxlength="30" name="item" required = "required"/>
								<span>Enter the name of the Item here</span>
							</li>
							</li>
							<li>
								<label for="quantity">Quantity</label>
								<input type="text" maxlength="30" name="quantity" required = "required"/>
								<span>Enter the quantity of the Item here</span>
							</li>
	
							<li>
								<label for="ui">UI</label>
								<input type="text" maxlength="30" name="ui" required = "required"/>
								<span>Enter the Unit of Issue here</span>
							</li>
							<li>
								<label for="cost">Cost</label>
								<input type="number" min="1" step="any" pattern="(^\\$?(([1-9](\\d*|\\d{0,2}(,\\d{3})*))|0)(\\.\\d{1,2})?$)" name="cost" required = "required"/>
								<span>Enter how much the item cost here</span>
							</li>
							<li>
								<label for="purchasedate">Purchase Date</label>
								<input type="date" name="purchasedate" required = "required"/>
								<span>Enter the date of purchase</span>
							</li>
							<li>
							<input type="submit" name="save" value="Save"/>
							<input type="reset" name="reset" value="Reset"/>
							</ul>
						</form>
				</fieldset>
		</body>
</html>