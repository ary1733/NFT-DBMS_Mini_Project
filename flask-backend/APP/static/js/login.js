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
      Email_Id: email,
      Password: password,
    }),
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      console.log(data);
      if (data.message == "success") {
        next_url = document.getElementById('next_url').value;
        window.location.href = next_url;
      } else {
        document.getElementById("error").innerHTML =
          "Invalid email or password";
      }
    })
    .catch(function (error) {
      console.log(error);
    });
});
