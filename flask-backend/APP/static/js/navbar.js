searchinput = document.getElementByClass("searchinput");
searchbtn = document.getElementByClass("searchbtn");

// On search btn clicked
searchbtn.addEventListener("click", function (event) {
    searchinput = searchinput.value;
    console.log(searchinput);
    // Send data to flask server
    fetch("/api/item/search", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        }
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          console.log(data);
          
        })
        .catch(function (error) {
          console.log(error);
        });
    });


