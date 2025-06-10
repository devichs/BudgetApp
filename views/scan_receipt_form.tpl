%# views/scan_receipt_form.tpl
% rebase('base.tpl', title='Scan New Receipt', load_base_style=True, current_year=current_year)

<h2>Upload a Receipt to Scan</h2>

<form action="/scan_receipt" method="post" enctype="multipart/form-data">
    <div>
        <label for="receipt_image">Select Receipt File (PDF, JPG, PNG):</label>
        <input type="file" id="receipt_image" name="receipt_image" accept="image/png, image/jpeg, application/pdf" required>
    </div>
    <br>
    <div>
        <input type="submit" value="Scan Receipt">
    </div>
</form>