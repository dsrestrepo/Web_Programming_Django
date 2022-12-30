document.addEventListener('DOMContentLoaded', function() {

    
    // Hit like like_button
    document.querySelectorAll('.like_button').forEach(button => {
        button.onclick = () => {
            //unlike
            if (button.classList.contains('btn-danger')){                    
                let id=button.dataset.id;
                let like = button.dataset.likes;
                console.log(like)
                like = parseInt(like) - 1
                console.log(like)
                console.log(id)

                fetch(`/like/${id}`, {
                    method: "PUT",
                    body: JSON.stringify({
                    like: false,
                    })
                })
                .then(response => response.json())
                .then(result => {
                if ("message" in result) {  
                    //if is success update the button
                    console.log(result['message'])
                    button.className='btn btn-primary like_button';
                    button.innerHTML=`like: ${like}`;
                    button.dataset.likes = like;
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

            }//like
            else{    
                let id=button.dataset.id;
                let like = button.dataset.likes;
                console.log(like)
                like = parseInt(like) + 1
                console.log(like)
                console.log(id)
                fetch(`/like/${id}`, {
                    method: "PUT",
                    body: JSON.stringify({
                    like: true,
                    }),
                })
                .then(response => response.json())
                .then(result => {
                if ("message" in result) {  
                    //if is success update the button
                    console.log(result['message'])
                    button.className='btn btn-danger like_button';
                    button.innerHTML=`unlike: ${like}`;
                    button.dataset.likes = like;
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
});
