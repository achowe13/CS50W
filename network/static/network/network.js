document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.onclick = function() {
            console.log(this.dataset.id);
            const post_id = this.dataset.id;
            console.log(post_id);
            document.querySelector(`#post-content-${post_id}`).style.display = 'none';
            document.querySelector(`#edit-form-${post_id}`).style.display = 'block';
        }
    });

    document.querySelectorAll('.save-btn').forEach(btn => {
        btn.onclick = function(event) {
            event.preventDefault();
            const post_id = this.dataset.id;
            console.log(post_id)
            Edit(post_id);
            
            //change content of post to text area and add a submit button where edit used to be
            document.querySelector(`#post-content-${post_id}`).style.display = 'block';
            document.querySelector(`#edit-form-${post_id}`).style.display = 'none';
        }
    });

    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.onclick = function(event) {
            event.preventDefault();
            const post_id = this.dataset.id;
            console.log(`post id is ${post_id}`);
            like(post_id);
        }
    })
})


function Edit(post_id) {
    
    
    //submit sends contents and post_id with csrf token to '/edit' 
    
    //does not refresh page and shows editted post
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    var edited_content = document.querySelector(`#edit-content-${post_id}`).value;
    console.log(edited_content)
    fetch('/edit', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            content: edited_content,
            post_id: post_id,
        })
    })
    .then(response => {
        if (response.status == 200) {
            document.querySelector(`#post-content-${post_id}`).innerHTML = edited_content;
        }
        else {
            alert('You are not authorized to edit this post.');
        }
        response.json();       
    })
    .then(result => {
        console.log(result);
    });
}


function like(post_id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    console.log(post_id);
    console.log({post_id})
    fetch('/like', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            post_id: post_id,
        })
    })
    .then(response => response.json())
    .then(data => {
        document.querySelector(`#like-count-${post_id}`).innerHTML = data.likes_count
    })
}