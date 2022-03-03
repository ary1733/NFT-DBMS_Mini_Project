submitform = document.getElementById("submitform");

// Get email and password from form on submit event
submitform.addEventListener("submit", function(event){
    event.preventDefault();

    email = document.getElementById("floatingInput").value;
    password = document.getElementById("form-floating").value;

    // Send data to flask server
    fetch({
        url: "/login",
        type: "POST",
        data: {
            email: email,
            password: password
        },
        success: function(data){
            if(data.success){
                window.location.href = "/";
            }else{
                alert("Login failed");
            }
        }
    });
});
