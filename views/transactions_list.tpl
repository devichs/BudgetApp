%# views/transactions_list.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year, page_specific_css=['transactions-list-style.css'])

<div class="transactions-list">
    <h2>Transactions List</h2>

    <form action="/transactions" method="get" class="filter-form">
        <div class="form-row">
            <div class="form-group">
                <p>Search Criteria</p>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="description">Description contains:</label>
                <input type="text" id="description" name="description" value="{{ description_filter or '' }}">
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="account">Core Account:</label>
                    <select id="account" name="core_account_id">
                        <option class="dropdown" value="">-- All Core Accounts --</option>
                        % for acc in all_accounts:
                            %# Pre-select the currently filtered account
                            <option class="dropdown" value="{{acc[0]}}" {{'selected' if str(acc[0]) == core_account_id_filter else ''}}>{{acc[1]}}</option>
                        % end
                    </select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group">
                <label for="start_date">Transaction From Date:</label>
                <input type="date" id="start_date" name="start_date" value="{{ start_date_filter or '' }}">
            </div>   
            <div class="form-group">
                <label for="end_date">Transaction To Date:</label>
                <input type="date" id="end_date" name="end_date" value="{{ end_date_filter or '' }}">
            </div>    
        </div>
        <div class="form-row">
            <div class="form-group">
                <input type="submit" value="Search"</>
                <input type="reset" name="reset" value="Reset"/> 
            </div>
        </div>
    </form>
</div>
    <table class="sortable centered">
        <thead>
            <tr>
                <th>Date</th>
                <th>Description</th>
                <th>Category</th>
                <th>Account</th>
                <th class="money">Amount</th>
                <th>Receipt</th>
            </tr>
        </thead>
        <tbody>
            % for tx in transactions:
            <tr>
                <td>{{tx[1]}}</td> <td>{{tx[2]}}</td> <td>{{tx[4] or 'Uncategorized'}}</td> <td>{{tx[5] or 'N/A'}}</td> <td class="money">${{ "{:,.2f}".format(tx[3]) }}</td> <td>
                    % if tx[6] == 1:
                        <a href="/view_receipt/{{tx[0]}}">(View)</a>
                    % else:
                        <a href="/scan_receipt/{{tx[0]}}">+ Add Receipt</a>
                    % end
                </td>
            </tr>
            % end
        </tbody>
    </table>

        <ul class="ulpagination">
    
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

                <li class="pages">
                    Page {{current_page}} of {{total_pages}}
                </li>
                <li class="navigationinstructions">
                    % if current_page > 1:
                        <a class="first" href="/transactions?page=1&{{query_params}}">&laquo; First</a>
                        <a class="previous" href="/transactions?page={{current_page - 1}}&{{query_params}}">&lsaquo; Previous</a>
                    % end

                    % if current_page < total_pages:
                        <a class="next" href="/transactions?page={{current_page + 1}}&{{query_params}}">Next &rsaquo;</a>
                        <a class="last" href="/transactions?page={{total_pages}}&{{query_params}}">Last &raquo;</a>
                    % end
                </li>
        </ul>

