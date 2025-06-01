<!DOCTYPE html>
<html>
	<head>
		<title>Receipts - Budget</title>
		<link rel = "stylesheet" href = "static\content\new-budget-style.css">
		<script src="static\scripts\sorttable.js"></script>
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
				<li class = "limenu"><a class = "amenu" href = "/budget">Go To Budget</a></li>
				<li class = "limenu"><a class = "amenu" href = "/list">Expense List</a></li>
				<li class = "limenu"><a class = "amenu" href = "/budget">Cancel New Expense</a></li>	
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/">Home</a></li>	
			</ul>
				<fieldset>
					<legend>Add a new item to the list:</legend>
						<form class = "new-item" action="/new" method="GET">
							<ul>
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
								<label for="ui">Unit of Issue</label>
								<select name="ui">
									<option value="AM - Ampoule">AM - Ampoule</option>
									<option value="AT - Assortment">AT - Assortment</option>
									<option value="AY - Assembly">AY - Assembly</option>
									<option value="BA - Ball">BA - Ball</option>
									<option value="BD - Bundle">BD - Bundle</option>
									<option value="BE - Bale">BE - Bale</option>
									<option value="BF - Board Foot">BF - Board Foot</option>
									<option value="BG - Bag">BG - Bag</option>
									<option value="BK - Book">BK - Book</option>
									<option value="BL - Barrel">BL - Barrel</option>
									<option value="BO - Bolt">BO - Bolt</option>
									<option value="BQ - Briquet">BQ - Briquet</option>
									<option value="BR - Bar">BR - Bar</option>
									<option value="BT - Bottle">BT - Bottle</option>
									<option value="BX - Box">BX - Box</option>
									<option value="CA - Cartridge">CA - Cartridge</option>
									<option value="CB - Carboy">CB - Carboy</option>
									<option value="CC - Cubic Centimeter">CC - Cubic Centimeter</option>
									<option value="CD - Cubic Yard">CD - Cubic Yard</option>
									<option value="CE - Cone">CE - Cone</option>
									<option value="CF - Cubic Foot">CF - Cubic Foot</option>
									<option value="CG - Centigram">CG - Centigram</option>
									<option value="CI - Cubic Inch">CI - Cubic Inch</option>
									<option value="CK - Cake">CK - Cake</option>
									<option value="CL - Coil">CL - Coil</option>
									<option value="CM - Centimeter">CM - Centimeter</option>
									<option value="CN - Can">CN - Can</option>
									<option value="CO - Container">CO - Container</option>
									<option value="CU - Curie">CU - Curie</option>
									<option value="CY - Cylinder">CY - Cylinder</option>
									<option value="CZ - Cubic Meter">CZ - Cubic Meter</option>
									<option value="DC - Decagram">DC - Decagram</option>
									<option value="DE - Decimeter">DE - Decimeter</option>
									<option value="DG - Decigram">DG - Decigram</option>
									<option value="DL - Deciliter">DL - Deciliter</option>
									<option value="DM - Dram">DM - Dram</option>
									<option value="DR - Drum">DR - Drum</option>
									<option value="DW - Pennyweight">DW - Pennyweight</option>
									<option value="DZ - Dozen">DZ - Dozen</option>
									<option value="EA - Each">EA - Each</option>
									<option value="EX - Exposure">EX - Exposure</option>
									<option value="FD - Fold">FD - Fold</option>
									<option value="FR - Frame">FR - Frame</option>
									<option value="FT - Foot">FT - Foot</option>
									<option value="FV - Five">FV - Five</option>
									<option value="FY - Fifty">FY - Fifty</option>
									<option value="GG - Great Gross">GG - Great Gross</option>
									<option value="GI - Gill">GI - Gill</option>
									<option value="GL - Gallon">GL - Gallon</option>
									<option value="GM - Gram">GM - Gram</option>
									<option value="GN - Grain">GN - Grain</option>
									<option value="GP - Group">GP - Group</option>
									<option value="GR - Gross">GR - Gross</option>
									<option value="HD - Hundred">HD - Hundred</option>
									<option value="HF - Hundred Feet">HF - Hundred Feet</option>
									<option value="HK - Hank">HK - Hank</option>
									<option value="HP - Hundred Pounds">HP - Hundred Pounds</option>
									<option value="HS - Hundred Square">HS - Hundred Square</option>
									<option value="HW - Hundred Weight">HW - Hundred Weight</option>
									<option value="HY - Hundred Yards">HY - Hundred Yards</option>
									<option value="IN - Inch">IN - Inchv
									<option value="JR - Jar">JR - Jar</option>
									<option value="KG - Kilogram">KG - Kilogram</option>
									<option value="KM - Kilometer">KM - Kilometer</option>
									<option value="KR - Carat">KR - Carat</option>
									<option value="KT - Kit">KT - Kit</option>
									<option value="LB - Pound">LB - Pound</option>
									<option value="LF - Linear Foot">LF - Linear Foot</option>
									<option value="LG - Length">LG - Length</option>
									<option value="LI - Liter">LI - Liter</option>
									<option value="LI - Liter">LI - Liter</option>
									<option value="MC - Thousand Cubic">MC - Thousand Cubic</option>
									<option value="MC - Thousand">MC - Thousand</option>
									<option value="ME - Meal">ME - Meal</option>
									<option value="MF - Thousand Feet">MF - Thousand Feet</option>
									<option value="MG - Milligram">MG - Milligram</option>
									<option value="MI - Mile">MI - Mile</option>
									<option value="ML - Milliliter">ML - Milliliter</option>
									<option value="MM - Millimeter">MM - Millimeter</option>
									<option value="MR - Meter">MR - Meter</option>
									<option value="MX - Thousand">MX - Thousand</option>
									<option value="OT - Outfit">OT - Outfit</option>
									<option value="OZ - Ounce">OZ - Ounce</option>
									<option value="PD - Pad">PD - Pad</option>
									<option value="PG - Package">PG - Package</option>
									<option value="PI - Pillow">PI - Pillow</option>
									<option value="PM - Plate">PM - Plate</option>
									<option value="PR - Pair">PR - Pair</option>
									<option value="PT - Pint">PT - Pint</option>
									<option value="PX - Pellet">PX - Pellet</option>
									<option value="PZ - Packet">PZ - Packet</option>
									<option value="QT - Quart">QT - Quart</option>
									<option value="RA - Ration">RA - Ration</option>
									<option value="RD - Round">RD - Round</option>
									<option value="RL - Reel">RL - Reel</option>
									<option value="RM - Ream">RM - Ream</option>
									<option value="RO - Roll">RO - Roll</option>
									<option value="RX - Thousand Rounds">RX - Thousand Rounds</option>
									<option value="SD - Skid">SD - Skid</option>
									<option value="SE - Set">SE - Set</option>
									<option value="SF - Square Foot">SF - Square Foot</option>
									<option value="SH - Sheet">SH - Sheet</option>
									<option value="SI - Square Inch">SI - Square Inch</option>
									<option value="SK - Skein">SK - Skein</option>
									<option value="SL - Spool">SL - Spool</option>
									<option value="SM - Square Meter">SM - Square Meter</option>
									<option value="SO - Shot">SO - Shot</option>
									<option value="SP - Strip">SP - Strip</option>
									<option value="SQ - Square">SQ - Square</option>
									<option value="SX - Stick">SX - Stick</option>
									<option value="SY - Square Yard">SY - Square Yard</option>
									<option value="TD - Twenty-four">TD - Twenty-four</option>
									<option value="TE - Ten">TE - Ten</option>
									<option value="TF - Twenty-five">TF - Twenty-five</option>
									<option value="TN - Ton (2,000 lb)">TN - Ton (2,000 lb)</option>
									<option value="TO - Troy Ounce">TO - Troy Ounce</option>
									<option value="TS - Thirty-six">TS - Thirty-six</option>
									<option value="TT - Tablet">TT - Tablet</option>
									<option value="TU - Tube">TU - Tube</option>
									<option value="US - U.S.P. Unit">US - U.S.P. Unit</option>
									<option value="VI - Vial">VI - Vial</option>
									<option value="YD - Yard">YD - Yard</option>
								</select>
								<span>Enter the Unit of Issue of the Item here</span>
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
</html>