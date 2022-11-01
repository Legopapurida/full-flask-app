function send_request(body, url) {
    fetch(url, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(body),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json",
        })
    }).then(function (response) {
        if (response.status !== 200 || response.status !== 201) {
            response.json().then(function (data) { alert(data["status"] + data["code"]); });
        } else {
            response.json().then(function (data) {
                alert(data)
                location.reload();
            });
        }

    });
}

function do_login() {
    var username = document.getElementById("username");
    var password = document.getElementById("password");

    var entry = {
        username: username.value,
        password: password.value,
    };
    send_request(entry, "auth/login");
}

function do_register() {
    var username = document.getElementById("username");
    var email = document.getElementById("email");
    var password = document.getElementById("password");
    var first_name = document.getElementById("first_name");
    var last_name = document.getElementById("last_name");

    var entry = {
        username: username.value,
        email: email.value,
        password: password.value,
        first_name: first_name.value,
        last_name: last_name.value,
    };

    send_request(entry, "auth/register");
}

function add_user() {
    var username = document.getElementById("username");
    var email = document.getElementById("email");
    var first_name = document.getElementById("first_name");
    var last_name = document.getElementById("last_name");

    var entry = {
        username: username.value,
        email: email.value,
        first_name: first_name.value,
        last_name: last_name.value,
    };

    send_request(entry, "account/register");
}