%# views/budget.tpl
% rebase('base.tpl', title='Budget - What\'s Left!', load_base_style=True, current_year=current_year, page_specific_css=['budget-style.css'])

	<nav class="page-navigation">
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
	</nav>
</html>