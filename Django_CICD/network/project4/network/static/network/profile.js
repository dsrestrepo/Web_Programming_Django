document.addEventListener('DOMContentLoaded', function() {
        
    // Hit follow
    document.querySelectorAll('.follow_button').forEach(button => {
        button.onclick = () => {
            //unfollow
            if (button.classList.contains('btn-outline-danger')){
                let number_followers = document.querySelector('#followers_count')
                let followers = number_followers.dataset.followers;
                followers = parseInt(followers) - 1
                console.log(followers)

                let username=button.dataset.username;
                console.log(username)
                fetch(`/follow/${username}`, {
                    method: "PUT",
                    body: JSON.stringify({
                    follow: false,
                    })
                })
                .then(response => response.json())
                .then(result => {
                if ("message" in result) {  
                    //if is success update the button and followers number
                    console.log(result['message'])
                    button.className='btn btn-outline-success follow_button';
                    button.innerHTML='follow';
                    number_followers.innerHTML=`followers: ${followers}`;
                    number_followers.dataset.followers=followers;
                }
                if ("error" in result) {
                    //if is not success
                    console.log(result['error'])
                }
                console.log(result);
                })
                .catch(error => {
                console.log(error);
                });        
                return false;
            }//follow
            else{
                let number_followers = document.querySelector('#followers_count')
                let followers = number_followers.dataset.followers;
                followers = parseInt(followers) + 1
                console.log(followers)
                let username=button.dataset.username;
                console.log(username)
                fetch(`/follow/${username}`, {
                    method: "PUT",
                    body: JSON.stringify({
                    follow: true,
                    })
                })
                .then(response => response.json())
                .then(result => {
                if ("message" in result) {  
                    //if is success update the button and followers number
                    console.log(result['message'])
                    button.className='btn btn-outline-danger follow_button';
                    button.innerHTML='unfollow';
                    number_followers.innerHTML=`followers: ${followers}`;
                    number_followers.dataset.followers=followers;
                }
                if ("error" in result) {
                    //if is not success
                    console.log(result['error'])
                }
                console.log(result);
                })
                .catch(error => {
                console.log(error);
                });        
                return false;
            }
        };
    });
    
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
            load_page()
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

