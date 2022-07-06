
function saveRecipe (rating) {
    const inputs = {

        title: document.querySelector('#title').textContent,
        ingredients: document.querySelector('#ingredients').textContent,
        instructions: document.querySelector('#instructions').textContent,
        image_path: document.querySelector('#image').value,
        source_url: document.querySelector('#source').value,
        rating: rating
    };
    // console.log(JSON.stringify(inputs))
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

    document.querySelector('#rate').addEventListener('submit', (evt) => {
        evt.preventDefault();
        const score = document.querySelector("#rating").value;
        saveRecipe(score);
    });
    
document.querySelector('#save').addEventListener('click', (evt) => {
    evt.preventDefault();
    saveRecipe();
});


  