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
						<form class = "new-item" action="/new" method="GET">
							<ul>
							<li>
								<label for="store">Store</label>
								<select name="store">	
									<option value="Wal Mart">Wal Mart</option>
									<option value="BJ's">BJ's</option>
									<option value="Global">Global</option>
									<option value="and That!">and That!</option>
									<option value="Costco">Costco</option>
									<option value="CVS">CVS</option>
									<option value="Dollar Store">Dollar Store</option>
								</select>
								<span>Enter the name of the Store here</span>
							</li>
							<li>
								<label for="category">Category</label>
									<select name="category">	
										<option value="Fruit">Fruit</option>
										<option value="Dairy">Dairy</option>
										<option value="Meat">Meat</option>
										<option value="Household Item">Household Item</option>
										<option value="Automotive">Automotive</option>
										<option value="Vegetable">Vegetable</option>
										<option value="Cereal">Cereal</option>
										<option value="Freezer Item">Freezer Item</option>
										<option value="Cracker">Cracker</option>
										<option value="Nuts">Nuts</option>
										<option value="Bread">Bread</option>
										<option value="Deli">Deli</option>
										<option value="Misc">Misc</option>
										<option value="Clothes">Clothes</option>
										<option value="MapleSyrup">MapleSyrup</option>
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
									<option value="AM">AM</option>
									<option value="AT">AT</option>
									<option value="AY">AY</option>
									<option value="BA">BA</option>
									<option value="BD">BD</option>
									<option value="BE">BE</option>
									<option value="BF">BF</option>
									<option value="BG">BG</option>
									<option value="BK">BK</option>
									<option value="BL">BL</option>
									<option value="BO">BO</option>
									<option value="BQ">BQ</option>
									<option value="BR">BR</option>
									<option value="BT">BT</option>
									<option value="BX">BX</option>
									<option value="CA">CA</option>
									<option value="CB">CB</option>
									<option value="CC">CC</option>
									<option value="CD">CD</option>
									<option value="CE">CE</option>
									<option value="CF">CF</option>
									<option value="CG">CG</option>
									<option value="CI">CI</option>
									<option value="CK">CK</option>
									<option value="CL">CL</option>
									<option value="CM">CM</option>
									<option value="CN">CN</option>
									<option value="CO">CO</option>
									<option value="CU">CU</option>
									<option value="CY">CY</option>
									<option value="RA">RA</option>
									<option value="CZ">CZ</option>
									<option value="DC">DC</option>
									<option value="DE">DE</option>
									<option value="DG">DG</option>
									<option value="DL">DL</option>
									<option value="DM">DM</option>
									<option value="DR">DR</option>
									<option value="DW">DW</option>
									<option value="DZ">DZ</option>
									<option value="EA">EA</option>
									<option value="EX">EX</option>
									<option value="FD">FD</option>
									<option value="FR">FR</option>
									<option value="FT">FT</option>
									<option value="FV">FV</option>
									<option value="FY">FY</option>
									<option value="GG">GG</option>
									<option value="GI">GI</option>
									<option value="GL">GL</option>
									<option value="GM">GM</option>
									<option value="GN">GN</option>
									<option value="GP">GP</option>
									<option value="GR">GR</option>
									<option value="HD">HD</option>
									<option value="HF">HF</option>
									<option value="HK">HK</option>
									<option value="HP">HP</option>
									<option value="HS">HS</option>
									<option value="HW">HW</option>
									<option value="HY">HY</option>
									<option value="IN">IN</option>
									<option value="JR">JR</option>
									<option value="KG">KG</option>
									<option value="KM">KM</option>
									<option value="KR">KR</option>
									<option value="KT">KT</option>
									<option value="LB">LB</option>
									<option value="LF">LF</option>
									<option value="LG">LG</option>
									<option value="LI">LI</option>
									<option value="LI">LI</option>
									<option value="MC">MC</option>
									<option value="MC">MC</option>
									<option value="ME">ME</option>
									<option value="MF">MF</option>
									<option value="MG">MG</option>
									<option value="MI">MI</option>
									<option value="ML">ML</option>
									<option value="MM">MM</option>
									<option value="MR">MR</option>
									<option value="MX">MX</option>
									<option value="OT">OT</option>
									<option value="OZ">OZ</option>
									<option value="PD">PD</option>
									<option value="PG">PG</option>
									<option value="PI">PI</option>
									<option value="PM">PM</option>
									<option value="PR">PR</option>
									<option value="PT">PT</option>
									<option value="PX">PX</option>
									<option value="PZ">PZ</option>
									<option value="QT">QT</option>
									<option value="RD">RD</option>
									<option value="RL">RL</option>
									<option value="RM">RM</option>
									<option value="RO">RO</option>
									<option value="RX">RX</option>
									<option value="SD">SD</option>
									<option value="SE">SE</option>
									<option value="SF">SF</option>
									<option value="SH">SH</option>
									<option value="SI">SI</option>
									<option value="SK">SK</option>
									<option value="SL">SL</option>
									<option value="SM">SM</option>
									<option value="SO">SO</option>
									<option value="SP">SP</option>
									<option value="SQ">SQ</option>
									<option value="SX">SX</option>
									<option value="SY">SY</option>
									<option value="TD">TD</option>
									<option value="TE">TE</option>
									<option value="TF">TF</option>
									<option value="TN">TN</option>
									<option value="TO">TO</option>
									<option value="TS">TS</option>
									<option value="TT">TT</option>
									<option value="TU">TU</option>
									<option value="US">US</option>
									<option value="VI">VI</option>
									<option value="YD">YD</option>
								</select>
								<span>Enter the Unit of Issue of the Item here</span>
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