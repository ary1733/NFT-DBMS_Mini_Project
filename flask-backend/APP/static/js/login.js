submitform = document.getElementById("submitform");

// Get email and password from form on submit event
submitform.addEventListener("submit", function (event) {
  event.preventDefault();

  email = document.getElementById("floatingInput").value;
  password = document.getElementById("form-floating").value;

  console.log(email);
    console.log(password);
  // Send data to flask server
  fetch("/api/user/login/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      email: email,
      password: password,
    }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data);
      if (data.message == "success") {
        window.location.href = "/account";
      } else {
        document.getElementById("error").innerHTML =
          "Invalid email or password";
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});
