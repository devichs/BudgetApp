%# views/index.tpl
% rebase('base.tpl', title='New Budget - What\'s Left!', load_base_style=True, current_year=current_year, page_specific_css=['update-budget-style.css'])
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
			<ul class = "ulmenu">
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/budget">Budget</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/">Home</a></li>
				<li class = "limenu"><a class = "amenu" href = "http://localhost:5555/budget">Cancel</a></li>
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