document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('form').onsubmit = ()=> {
        const user = document.querySelector('#username').value;

        fetch(`/users/${user}`)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            username=data.username
            if (username === undefined) {
                console.log('error')
                document.querySelector('#result').innerHTML = "User not found"
                document.querySelector('#result').style.color="red"
            }else{
                const result = `
                <div class="alert alert-success" role="alert">
                <a href="/profile/${username}" style="font-size: 20px; color:green">${username}</a>
                </div> `;
                document.querySelector('#result').innerHTML = result;
            }
        })
        .catch(error => {
            console.log('Error:', error);
        });
        return false;
    }
});
