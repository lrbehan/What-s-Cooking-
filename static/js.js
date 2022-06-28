document.querySelector('#save').addEventListener('click', (evt) => {
    evt.preventDefault();
    
    const inputs = {

        title: document.querySelector('#title').textContent,
        ingredients: document.querySelector('#ingredients').textContent,
        instructions: document.querySelector('#instructions').textContent,
        image_path: document.querySelector('#image').value,
        source_url: document.querySelector('#source').value
    };

    fetch('/save', {
        method: 'POST',
        body: JSON.stringify(inputs),
        headers: {
        'Content-Type': 'application/json',
        },
    })
        .then((response) => response.text())
        .then((responsetext) => {
            alert("saved recipe");
        });
    });
    