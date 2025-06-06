%# views/list.tpl
% rebase('base.tpl', title='Expense List - What\'s Left!', load_base_style=True, page_specific_css=['list-style.css'])

<div class = "nav"><!--navigation menu-->
	<ul class = "nav">
		<li><a href = "/new">Add New Expense</a></li>
		<li><a href = "/budget">Go To Budget</a></li>
		<li><a href = "/list">Import Expense List</a></li>
		<li><a href = "http://localhost:5555/">Home</a></li>		
	</ul>
</div><!--end navigation menu-->
		% if rows:
		<table class = "sortable centered">
		<caption>Current list of items purchased</caption>
			<thead>
				<tr>
					<th>ID</th>
					<th>Store</th>
					<th>Category</th>
					<th>Item</th>
					<th>Quantity</th>
					<th>UI</th>
					<th>Cost</th>    
					<th>Purchase date</th>
					<th>Status</th>
				</tr>
			</thead>	
			<tbody>
				%for row in rows:
				<tr>
					<td>{{row[0]}}</td> 
					<td>{{row[1]}}</td>
					<td>{{row[2]}}</td> 
					<td>{{row[3]}}</td>
					<td>{{row[4]}}</td> 
					<td>{{row[5]}}</td>
					<td>{{row[6]}}</td> 
					<td>{{row[7]}}</td>
					<td>{{row[8]}}</td>
					<td>
						<a href="/edit/{{row[0]}}">Edit</a>
						%# todo add delete
					</td>
				</tr>
				% end
			</tbody>
		</table>
		% else:
		<p>No expenses found.</p>
		% end