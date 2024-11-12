document
  .getElementById("sayHelloButton")
  .addEventListener("click", function () {
    fetch(document.getElementById("sayHelloButton").getAttribute("data-url"))
      .then((response) => response.json())
      .then((data) => {
        console.log(data.message); // Prints "Hello World" in the browser console
        alert(data.message); // Display "Hello World" in an alert box
      })
      .catch((error) => console.error("Error:", error));
  });
