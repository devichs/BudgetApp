%# views/category_totals_report.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<div class="report-container">
    <h2>Category Totals (This Month)</h2>
    <div class="table-box">
        <table class="sortable" id="category-totals-table">
            <thead>
                <tr>
                    <th>Category</th>
                    <th class="money">Net Total</th>
                </tr>
            </thead>
            <tbody id="table-body">
                <tr><td colspan="2">Loading...</td></tr>
            </tbody>
        </table>
    </div>
</div>

<style>
    .report-container { max-width: 800px; margin: 20px auto; }
    .table-box { padding: 20px; border: 1px solid #ddd; border-radius: 5px; background: #fff; }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/category-totals')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('table-body');
            // Clear the "Loading..." message
            tableBody.innerHTML = ''; 

            if (data.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="2">No data for this period.</td></tr>';
                return;
            }

            // Loop through the data and create a table row for each category
            data.forEach(item => {
                const row = tableBody.insertRow();
                
                const cellCategory = row.insertCell();
                const cellTotal = row.insertCell();
                
                // Format the cells
                cellCategory.textContent = item.category_name || 'Uncategorized';
                cellTotal.textContent = '$' + parseFloat(item.net_total).toFixed(2);
                cellTotal.className = 'money'; // For right-aligning text
            });
            
            // Make the new table sortable (if you've included sorttable.js in base.tpl)
            if (typeof sorttable !== 'undefined') {
                const newTable = document.getElementById('category-totals-table');
                sorttable.makeSortable(newTable);
            }
        })
        .catch(error => {
            console.error('Error fetching category totals:', error);
            document.getElementById('table-body').innerHTML = '<tr><td colspan="2">Error loading data.</td></tr>';
        });
});
</script>