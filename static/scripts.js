document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');
    loginForm.addEventListener('submit', async function (event) {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const phone_number = document.getElementById('phone_number').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}&phone_number=${encodeURIComponent(phone_number)}`,
        });

        const data = await response.json();
        console.log(data);
        window.location.replace("http://127.0.0.1:8000/user-list");
    });
});
