%# views/manage_descriptions.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year, page_specific_css=['manage-descriptions-style.css'])

<div class="manage-descriptions">
    <h2>Manage Transaction Categorization</h2>
    <p>
        Select a new Main and Sub-Category for Transactions.
    </p>
    <p>
        Categories will be updated for all Transactions with the same Description.
    </p>    
</div>

<div class="table-box">
    <table>
        <thead>
            <tr>
                <th>Transaction Description</th>
                <th>Current Main Category</th>
                <th>Current Sub-Category</th>
                <th style="width: 400px;">New Category Assignment</th>
                <th style="width: 100px;">Action</th>
            </tr>
        </thead>
        <tbody>
            % for item in description_data:
            <tr>
                <td>{{item['description']}}</td>
                <td>{{item['main_category_name'] or 'N/A'}}</td>
                <td>{{item['sub_category_name'] or 'N/A'}}</td>
                <td>
                    <form action="/update/description_category" method="post" style="display: flex; gap: 10px;">
                        <input type="hidden" name="description" value="{{item['description']}}">
                        
                        <select name="main_category" class="main-category-select" style="flex: 1;">
                            <option value="">-- Select Main --</option>
                            % for cat in all_main_categories:
                            <option value="{{cat['main_category_id']}}">{{cat['main_category_name']}}</option>
                            % end
                        </select>
                        
                        <select name="sub_category_id" class="sub-category-select" style="flex: 1;">
                            <option value="">-- Select Sub --</option>
                            %# This will be populated by JavaScript
                        </select>
                </td>
                <td>
                        <button type="submit">Save</button>
                    </form>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>

<script>
    // 1. Get the full list of sub-categories from our Python route
    const allSubCategories = JSON.parse('{{!all_sub_categories_json}}');

    // 2. Find all the "Main Category" dropdowns on the page
    const mainCategorySelects = document.querySelectorAll('.main-category-select');

    // 3. Add a "change" event listener to each one
    mainCategorySelects.forEach(select => {
        select.addEventListener('change', function() {
            // Get the ID of the main category that was just selected
            const selectedMainId = this.value;

            // Find the corresponding sub-category dropdown in the same table row
            const row = this.closest('tr');
            const subCategorySelect = row.querySelector('.sub-category-select');

            // Clear out any existing options
            subCategorySelect.innerHTML = '<option value="">-- Select Sub --</option>';

            // Filter the full list of sub-categories to find the ones that match
            const relevantSubCategories = allSubCategories.filter(subCat => {
                return subCat.main_category_id == selectedMainId;
            });

            // Loop through the relevant sub-categories and add them as options
            relevantSubCategories.forEach(subCat => {
                const option = document.createElement('option');
                option.value = subCat.sub_category_id;
                option.textContent = subCat.sub_category_name;
                subCategorySelect.appendChild(option);
            });
        });
    });
</script>