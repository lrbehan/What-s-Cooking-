
function saveRecipe (rating) {
    console.log(document.querySelector('#title').textContent)
    const inputs = {

        title: document.querySelector('#title').textContent,
        ingredients: document.querySelector('#ingredients').textContent,
        instructions: document.querySelector('#instructions').textContent,
        image_path: document.querySelector('#image').value,
        source_url: document.querySelector('#source').value,
        rating: rating
    };
    console.log(inputs)
    console.log(JSON.stringify(inputs))
    fetch('/save', {
        method: 'POST',
        body: JSON.stringify(inputs),
        headers: {
        'Content-Type': 'application/json',
        },
    })
    .then((response) => response.json())
    .then((responseJson) => {
        alert(responseJson.status);
    });
    }


document.querySelector('#save').addEventListener('click', (evt) => {
    evt.preventDefault();
    saveRecipe()
})


    document.querySelector('#rate').addEventListener('click', (evt) => {
        evt.preventDefault();
        const score = document.querySelector("#rating").value
        saveRecipe(score)
    })