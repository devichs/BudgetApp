%# views/manage_categories.tpl
% rebase('base.tpl', title=title, load_base_style=True, current_year=current_year)

<h2>Manage Categories</h2>
<p>Here you can rename or delete existing categories.</p>

<div class="table-box">
    <table class="sortable">
        <thead>
            <tr>
                <th>Category Name</th>
                <th class="actions" style="width: 150px;">Actions</th>
            </tr>
        </thead>
        <tbody>
            % for cat_id, name in categories:
            <tr id="category-row-{{cat_id}}">
                <td data-field="name">{{name}}</td>
                <td class="actions">
                    <button type="button" class="edit-btn" data-id="{{cat_id}}" data-name="{{name}}">Edit</button>
                    <button type="button" class="delete-btn" data-id="{{cat_id}}" data-name="{{name}}">Delete</button>
                </td>
            </tr>
            % end
        </tbody>
    </table>
</div>

<style>
    .actions { text-align: center; }
    .actions button { margin: 0 5px; }
    /* Style for the input field when editing */
    td input[type="text"] { width: 95%; padding: 5px; }
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Attach event listeners to all Edit and Delete buttons
    const tableBody = document.querySelector('table tbody');

    tableBody.addEventListener('click', function(event) {
        const target = event.target;

        if (target.classList.contains('delete-btn')) {
            handleDelete(target);
        } else if (target.classList.contains('edit-btn')) {
            handleEdit(target);
        } else if (target.classList.contains('save-btn')) {
            handleSave(target);
        } else if (target.classList.contains('cancel-btn')) {
            handleCancel(target);
        }
    });
});

function handleEdit(button) {
    const categoryId = button.dataset.id;
    const row = document.getElementById(`category-row-${categoryId}`);
    const nameCell = row.querySelector('td[data-field="name"]');
    const currentName = nameCell.textContent;

    // Replace cell content with an input field
    nameCell.innerHTML = `<input type="text" value="${currentName}" style="width: 90%;">`;
    nameCell.firstChild.focus(); // Focus on the new input field

    // Replace buttons
    const actionsCell = button.parentNode;
    actionsCell.innerHTML = `
        <button type="button" class="save-btn" data-id="${categoryId}" data-original-name="${currentName}">Save</button>
        <button type="button" class="cancel-btn" data-id="${categoryId}" data-original-name="${currentName}">Cancel</button>
    `;
}

function handleSave(button) {
    const categoryId = button.dataset.id;
    const row = document.getElementById(`category-row-${categoryId}`);
    const inputField = row.querySelector('input[type="text"]');
    const newName = inputField.value.trim();

    if (!newName) {
        alert('Category name cannot be empty.');
        return;
    }

    // Send the update to the backend
    fetch(`/update/category/${categoryId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: newName }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update successful, revert UI back to normal text
            const nameCell = inputField.parentNode;
            nameCell.textContent = newName;
            
            const actionsCell = button.parentNode;
            actionsCell.innerHTML = `
                <button type="button" class="edit-btn" data-id="${categoryId}" data-name="${newName}">Edit</button>
                <button type="button" class="delete-btn" data-id="${categoryId}" data-name="${newName}">Delete</button>
            `;
        } else {
            alert('Error updating category: ' + data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function handleCancel(button) {
    const categoryId = button.dataset.id;
    const originalName = button.dataset.originalName;
    const row = document.getElementById(`category-row-${categoryId}`);
    const nameCell = row.querySelector('td[data-field="name"]');
    
    // Revert the cell content and buttons
    nameCell.textContent = originalName;
    const actionsCell = button.parentNode;
    actionsCell.innerHTML = `
        <button type="button" class="edit-btn" data-id="${categoryId}" data-name="${originalName}">Edit</button>
        <button type="button" class="delete-btn" data-id="${categoryId}" data-name="${originalName}">Delete</button>
    `;
}

function handleDelete(button) {
    const categoryId = button.dataset.id;
    const categoryName = button.dataset.name;

    if (confirm(`Are you sure you want to delete the category "${categoryName}"? All associated transactions will become "Uncategorized".`)) {
        fetch(`/delete/category/${categoryId}`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // If successful, remove the row from the page directly
                document.getElementById(`category-row-${categoryId}`).remove();
            } else {
                alert('Error deleting category: ' + data.message);
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
</script>