var i = 1;

document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname == '/new_recipe') {
        document.querySelector('#add-btn').addEventListener('click', add_both_box);
    }
    else if (window.location.href.indexOf('recipe_page') > -1) {
        //user_rating = 
        //console.log(user_rating)
        document.querySelector('#new-comment-btn').addEventListener('click', New_Comment);
        document.getElementsByName('rating').forEach(input => {
            input.addEventListener('change', Rate)
        });
    }
    else {
       document.querySelector('#add-btn').addEventListener('click', add_ingredient_box); 
    }
    

})

function add_both_box(event) {
    console.log('logged')
    event.preventDefault()
    
    let new_both_box = document.createElement('div')
    new_both_box.className = 'ingredient-row';
    new_both_box.innerHTML = 
        `<div class="ingredient-column-1" style="flex: 50%; text-align: right; padding: 10px"><input type="text" name="measurement[${i}]" placeholder="Measurement" style="margin: 0px; border-radius: 20px; padding: 5px"></div>
        <div class="ingredient-column-2" style="flex: 50%; text-align: left; padding: 10px"><input class="ingredient-box" list="ingredients" name="ingredient[${i}]" style="margin: 0px; border-radius: 20px; padding: 5px" placeholder="Ingredient"></div>`
    document.querySelector('#extra-box').append(new_both_box);
    
    i++
    console.log(i)
}

function add_ingredient_box(event) {
    console.log('logged')
    event.preventDefault()
    
    let new_ingredient_box = document.createElement('input')
    new_ingredient_box.className = 'ingredient-box';
    new_ingredient_box.setAttribute('list', 'ingredients')
    new_ingredient_box.setAttribute('name', `ingredient[${i}]`)
    new_ingredient_box.setAttribute('class', 'ingredient-box')
    new_ingredient_box.setAttribute('style', 'margin:10px; border-radius: 20px; padding: 5px')
    document.querySelector('#extra-box').append(new_ingredient_box);

    i++
    console.log(i)
}

let displayed = false;

function New_Comment(event) {
    event.preventDefault()
    
    if (displayed == false) {
        document.querySelector('#new-comment-div').style.display = 'block';
        displayed = true;
        document.querySelector('#new-comment-btn').innerHTML = 'Hide Comment Box'
    }
    else {
        document.querySelector('#new-comment-div').style.display = 'none';
        displayed = false;
        document.querySelector('#new-comment-btn').innerHTML = 'New Comment'
    }
    console.log(displayed)
}

function Rate() {

    const page_id = document.querySelector('.stars-inputs').getAttribute('data-page_id');

    var rating = this.value;
    var csrftoken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    
    fetch('/rate', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            rating: rating,
            page_id: page_id,
        })
    })
    .then (response => {
        if (response.ok) {
            console.log('success');
        }
    });
}