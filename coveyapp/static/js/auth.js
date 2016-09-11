var auth = auth || {};

function user_exists(nickname) {

};

function login_init(logindiv) {
    var frm = $(logindiv);
    frm.submit(function(e) {
        var formData = {};
        frm.serializeArray().map(function(row) {
            formData[row.name] = row.value;
        });

        // if this user already exists, request token
        if (user_exists(formData['nickname'])) {
            request_token(formData['nickname'], formData['password']);
        } else {
            // try and create user and request token
            formData = JSON.stringify(formData);
            $.ajax({
                method: frm.attr('method'),
                url: frm.attr('action'),
                data: formData,
                dataType: "json",
                contentType: "application/json",
                success: function(data) {
                    console.log(data);
                    // get the token
                    auth.token = get_token(null, null);
                },
                error: function(data) {
                    console.log(data);
                }
            });
        }

        e.preventDefault();
    });
}

function get_token(u, p) {
    console.log("getting token");
}
