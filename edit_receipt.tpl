%#template for editing a task
%#the template expects to receive a value for "no" as well a "old", the text of the selected ToDo item
<p>Edit the task with ID = {{no}}</p>
<form action="/edit/{{no}}" method="get">
<label for = "store">Store</label>
<input type="text" name="store" value="{{old[0]}}" size="30" maxlength="30">
<label for = "category">Category</label>
<input type="text" name="category" value="{{old[0]}}" size="30" maxlength="30">
<label for = "item">Item</label>
<input type="text" name="item" value="{{old[0]}}" size="30" maxlength="30">
<label for = "quantity">Quantity</label>
<input type="text" name="quantity" value="{{old[0]}}" size="30" maxlength="30">
<label for = "ui">UI</label>
<input type="text" name="ui" value="{{old[0]}}" size="30" maxlength="30">
<label for = "cost">Cost</label>
<input type="text" name="cost" value="{{old[0]}}" size="30" maxlength="30">
<label for = "date">Date</label>
<input type="text" name="date" value="{{old[0]}}" size="30" maxlength="30">
<select name="status">
<option>open</option>
<option>closed</option>
</select>
<br/>
<input type="submit" name="save" value="save">
</form>