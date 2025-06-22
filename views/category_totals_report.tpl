%# views/category_totals_report.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<div class="report-container">
    <h2>Category Totals</h2>

    <form id="filter-form" class="filter-form">
        <div class="form-row">
            <div class="form-group">
                <label for="start_date">Start Date:</label>
                <input type="date" id="start_date" name="start_date" value="{{start_date}}">
            </div>
            <div class="form-group">
                <label for="end_date">End Date:</label>
                <input type="date" id="end_date" name="end_date" value="{{end_date}}">
            </div>
        </div>
        <div class="form-row">
            <button type="submit">Generate Report</button>
        </div>
    </form>
    
    <div class="table-box" style="margin-top: 20px;">
        <table class="sortable" id="category-totals-table">
            <thead>
                <tr>
                    <th>Sub-Category</th>
                    <th class="money">Net Total</th>
                </tr>
            </thead>
            <tbody id="table-body">
                <tr><td colspan="2">Select a date range and click "Generate Report".</td></tr>
            </tbody>
        </table>
    </div>
</div>

<style>
.report-container { max-width: 800px; margin: 20px auto; }
.table-box { padding: 20px; border: 1px solid #ddd; border-radius: 5px; background: #fff; }
.filter-form { background-color: #f7f7f7; border: 1px solid #ddd; padding: 15px; margin-bottom: 20px; border-radius: 5px; }
.filter-form .form-row { display: flex; gap: 20px; margin-bottom: 10px; justify-content: center; align-items: center; }
.filter-form .form-group { flex: 1; }
.filter-form label { display: block; margin-bottom: 5px; font-size: 14px; text-align: left;}
.filter-form input, .filter-form button { width: 100%; padding: 8px; box-sizing: border-box; }
</style>

<script>
// Wait for the page to load
document.addEventListener('DOMContentLoaded', function() {
    
    // Find the form
    const filterForm = document.getElementById('filter-form');

    // Add an event listener for when the form is submitted
    filterForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the form from doing a full page reload

        // Get the date values from the form inputs
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;
        const tableBody = document.getElementById('table-body');
        
        if (!startDate || !endDate) {
            alert('Please select both a start and end date.');
            return;
        }

        tableBody.innerHTML = '<tr><td colspan="2">Loading...</td></tr>';

        // Fetch data from our API, now with the dates as URL parameters
        fetch(`/api/category-totals?start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {
                // Clear the "Loading..." message
                tableBody.innerHTML = ''; 

                if (data.length === 0) {
                    tableBody.innerHTML = '<tr><td colspan="2">No data for this period.</td></tr>';
                    return;
                }

                data.forEach(item => {
                    const row = tableBody.insertRow();
                    const cellCategory = row.insertCell();
                    const cellTotal = row.insertCell();
                    
                    cellCategory.textContent = item.sub_category_name || 'Uncategorized';
                    cellTotal.textContent = '$' + parseFloat(item.net_total).toFixed(2);
                    cellTotal.className = 'money';
                });
                
                if (typeof sorttable !== 'undefined') {
                    const newTable = document.getElementById('category-totals-table');
                    sorttable.makeSortable(newTable);
                }
            })
            .catch(error => {
                console.error('Error fetching category totals:', error);
                tableBody.innerHTML = '<tr><td colspan="2">Error loading data.</td></tr>';
            });
    });
});
</script>