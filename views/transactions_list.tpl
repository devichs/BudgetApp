%# views/transactions_list.tpl
% rebase('base.tpl', title=title, load_base_style=True)

<h2>All Transactions</h2>

<form action="/transactions" method="get" class="filter-form">
    <div class="form-row">
        <div class="form-group">
            <label for="description">Description contains:</label>
            <input type="text" id="description" name="description" value="{{ description_filter or '' }}">
        </div>
        <div class="form-group">
            <label for="account">Account:</label>
            <select id="account" name="core_account_id">
                <option value="">-- All Accounts --</option>
                % for acc in all_accounts:
                    %# Pre-select the currently filtered account
                    <option value="{{acc[0]}}" {{'selected' if str(acc[0]) == core_account_id_filter else ''}}>{{acc[1]}}</option>
                % end
            </select>
        </div>
    </div>
    <div class="form-row">
        <div class="form-group">
            <label for="start_date">From Date:</label>
            <input type="date" id="start_date" name="start_date" value="{{ start_date_filter or '' }}">
        </div>
        <div class="form-group">
            <label for="end_date">To Date:</label>
            <input type="date" id="end_date" name="end_date" value="{{ end_date_filter or '' }}">
        </div>
    </div>
    <div class="form-row">
        <button type="submit">Search</button>
        <a href="/transactions">Clear Filters</a>
    </div>
</form>

<style>
/* Simple styling for the form */
.filter-form { background-color: #f7f7f7; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
.filter-form .form-row { display: flex; gap: 20px; margin-bottom: 10px; }
.filter-form .form-group { flex: 1; }
.filter-form label { display: block; margin-bottom: 5px; font-size: 14px; }
.filter-form input, .filter-form select, .filter-form button { width: 100%; padding: 8px; box-sizing: border-box; }
</style>

<table class="sortable">
    <thead>
        <tr>
            <th>Date</th>
            <th>Description</th>
            <th>Category</th>
            <th>Account</th>
            <th class="money">Amount</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % for tx in transactions:
        <tr>
            <td>{{tx[1]}}</td> <td>{{tx[2]}}</td> <td>{{tx[4] or 'Uncategorized'}}</td> <td>{{tx[5] or 'N/A'}}</td> <td class="money">${{ "{:,.2f}".format(tx[3]) }}</td> <td>
                %# <a href="/edit_transaction/{{tx[0]}}">Edit</a> - Placeholder for future edit link
            </td>
        </tr>
        % end
    </tbody>
</table>

%# ... your </table> for transactions ...

<div class="pagination">
    
    %# --- NEW ROBUST CODE ---
    %# Build a query string that includes only the active filters
    % params = []
    % if description_filter:
    %   params.append('description=' + description_filter)
    % end
    % if core_account_id_filter:
    %   params.append('core_account_id=' + core_account_id_filter)
    % end
    % if start_date_filter:
    %   params.append('start_date=' + start_date_filter)
    % end
    % if end_date_filter:
    %   params.append('end_date=' + end_date_filter)
    % end
    % query_params = '&'.join(params)
    %# --- END OF NEW CODE ---

    Page {{current_page}} of {{total_pages}}
    <br><br>

    % if current_page > 1:
        <a href="/transactions?page=1&{{query_params}}">&laquo; First</a>
        <a href="/transactions?page={{current_page - 1}}&{{query_params}}">&lsaquo; Previous</a>
    % end

    % if current_page < total_pages:
        <a href="/transactions?page={{current_page + 1}}&{{query_params}}">Next &rsaquo;</a>
        <a href="/transactions?page={{total_pages}}&{{query_params}}">Last &raquo;</a>
    % end
</div>

<style>
/* Simple styling for pagination links */
.pagination { margin-top: 20px; text-align: center; }
.pagination a { padding: 5px 10px; border: 1px solid #ddd; text-decoration: none; color: #080808; }
.pagination a:hover { background-color: #efefef; }
</style>