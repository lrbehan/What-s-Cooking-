
const editBtn = document.querySelector("#edit");
displayedIngredients = document.querySelector('#ingredients')
displayedInstructions = document.querySelector('#instructions')

editBtn.addEventListener('click', (evt) => {
    evt.preventDefault();
    
    originalIngredients = document.querySelector('#ingredients').innerText;
    originalInstructions = document.querySelector('#instructions').innerText;
    title = document.querySelector('#title').textContent;
    source_url = document.querySelector('#source_url').value;
    image = document.querySelector('#image').value;

    displayedIngredients.hidden = "hidden";
    displayedInstructions.hidden = "hidden";
    editBtn.hidden = "hidden";

    document.querySelector('#edit_recipe').insertAdjacentHTML('beforeend', `
    <form id="edit_recipe_form" action="/edit_recipe" method="POST">
    
    <p style="margin-left: 60px"><button id="save_updated_recipe">Save Edited Recipe</button></p> 
    
    <p><textarea name="edit_ingredients" style="width:75%; height: 400px; margin-left: 60px"> ${originalIngredients} </textarea><p/>
    <textarea name="edit_instructions" style="width:75%; height: 400px; margin-left: 60px"> ${originalInstructions} </textarea>
    <input type="hidden" name="title" value="${title}"></input>
    <input type="hidden" name="source_url" value="${source_url}"></input>
    <input type="hidden" name="image" value="${image}"></input>
    </form>
    `)
  });
