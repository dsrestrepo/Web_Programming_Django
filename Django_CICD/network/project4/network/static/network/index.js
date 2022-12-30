document.addEventListener('DOMContentLoaded', function() {
        
    // New Post
    document.querySelector('#post-form').onsubmit = ()=>{
        let post = document.querySelector('#post-content').value;
        fetch('/newPost', {
            method: 'POST',
            body: JSON.stringify({
                content: post,
            })
          })        
        .then(response => response.json())
        .then(result => {
        if ("message" in result) {  
            console.log(result['message'])
            document.querySelector('#post-content').value="";
            location.reload();
            //if is success send to sent view
        }
        if ("error" in result) {
            console.log(result['error'])
            //if is not success show the error
            document.querySelector('#result').innerHTML = result['error']
        }
        console.log(result);
        })
        .catch(error => {
        console.log(error);
        });
        return false;
    };


    // Hit edit (on the post)
    document.querySelectorAll('.btn-warning').forEach(button => {
        button.onclick = () => {
            let post_id = button.dataset.id;
            let post_content = document.querySelector(`#content-${post_id}`).textContent;
            console.log(post_id)
            console.log(post_content)
            edit_post(post_id,post_content)
        };
    
    });

    // Edit Post
    document.querySelector('#edit-form').onsubmit = ()=>{
        let post = document.querySelector('#edit-content').value;
        let id = document.querySelector('#post_id').value;
        fetch(`/edit_post/${id}`, {
            method: "PUT",
            body: JSON.stringify({
            content: post,
            })
        })
        .then(response => response.json())
        .then(result => {
        if ("message" in result) {  
            console.log(result['message'])
            document.querySelector(`#content-${id}`).textContent=post
            load_page_inlocation(id)
            //if is success send to sent view
        }
        if ("error" in result) {
            console.log(result['error'])
            //if is not success show the error
            document.querySelector('#result_edit').innerHTML = result['error']
        }
        console.log(result);
        })
        .catch(error => {
        console.log(error);
        });
        return false;        
    };

    //by default
    load_page()
});


function edit_post(post_id, post_content) {
    // Show edit, hide posts
    document.querySelector('#edit-form').style.display = 'flex';
    document.querySelector('#post-form').style.display = 'none';
    document.querySelector('.posts-all').style.display = 'none';
    
    // Clear out composition fields
    document.querySelector('#edit-content').value = post_content;
    document.querySelector('#post_id').value = post_id;
}

function load_page() {
    // by default don't show the edit box
    document.querySelector('#edit-form').style.display = 'none';
    document.querySelector('#post-form').style.display = 'flex';
    document.querySelector('.posts-all').style.display = 'flex';

}

function load_page_inlocation(id) {
    // show the edited post
    document.querySelector('#edit-form').style.display = 'none';
    document.querySelector('#post-form').style.display = 'flex';
    document.querySelector('.posts-all').style.display = 'flex';
    window.location.hash = `card-${id}`;
}
