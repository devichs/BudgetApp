%# views/new-receipt.tpl
% rebase('base.tpl', title='New Receipts - What\'s Left!', current_year=current_year, load_base_style=True, page_specific_css=['new-style.css'])

	<head> 
		<script type="text/javascript">
		<!-- auto expand textarea -->
		function adjust_textarea(h) {
			h.style.height = "20px";
			h.style.height = (h.scrollHeight)+"px";
		}
		</script>
	</head>
		<body>
			<ul class = "ulmainmenu">
				<li class = "limainmenu"><a class = "amenu" href = "/budget">Go To Budget</a></li>
				<li class = "limainmenu"><a class = "amenu" href = "/list">View Expense List</a></li>
				<li class = "limainmenu"><a class = "amenu" href = "/budget">Cancel New Expense</a></li>	
				<li class = "limainmenu"><a class = "amenu" href = "http://localhost:5555/">Home</a></li>	
			</ul>
				<fieldset>
					<legend>Add a new item to the expense list:</legend>
						<form class = "new-item" action="/new" method="GET">
							<ul class = "ulnewitemenu">
							<li>
								<label for="store">Store</label>
								<select name="store">	
									<option value="99 cent Store">99 cent Store</option>
									<option value="Aldi's">Aldi's</option>
									<option value="Cash and Carry">Cash and Carry</option>
									<option value="Costco">Costco</option>
									<option value="CVS">CVS</option>
									<option value="Dollar Store">Dollar Store</option>
									<option value="Target">Target</option>
									<option value="Wal Mart">Wal Mart</option>
									<option value="Winco">Winco</option>
									<option value="Sams">Sam's</option>
									<option value="Whole Foods">Whole Foods</option>
									<option value="Burger King">Burger King</option>
									<option value="McDonalds">McDonalds</option>
									<option value="Kohls">Kohls</option>
									<option value="Little Caesar's">Little Caesar's</option>
									<option value="Pizza Hut">Pizza Hut</option>
									<option value="Other Restaurant">Other Restaurant</option>
									<option value="Other Fast Food">Other Fast Food</option>
									
								</select>
								<span>Enter the name of the Store here</span>
							</li>
							<li>
								<label for="category">Category</label>
									<select name="category">	
										<option value="Apparel">Apparel</option>
										<option value="Automotive">Automotive</option>
										<option value="Bakery">Bakery</option>
										<option value="Bathroom Item">Bathroom Item</option>
										<option value="Beverage">Beverage</option>
										<option value="Dairy">Dairy</option>
										<option value="Deli">Deli</option>
										<option value="Dry Goods">Dry Goods</option>
										<option value="Food Spice">Food Spice</option>
										<option value="Freezer Item">Freezer Item</option>
										<option value="Fruit">Fruit</option>
										<option value="Garden">Garden</option>
										<option value="Grocery">Grocery</option>
										<option value="Health And Beauty">Health And Beauty</option>
										<option value="Household Item">Household Item</option>
										<option value="Kitchen Item">Kitchen Item</option>
										<option value="Meat">Meat</option>
										<option value="Medical Item">Medical Item</option>
										<option value="Vegetable">Vegetable</option>
										<option value="Restaurant">Restaurant</option>
										<option value="Fast Food">Fast Food</option>
									</select>
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
								<label for="cost">Cost</label>
								<input type="number" step="any" pattern="(^\\$?(([1-9](\\d*|\\d{0,2}(,\\d{3})*))|0)(\\.\\d{1,2})?$)" name="cost" required = "required"/>
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