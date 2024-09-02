document
  .getElementById("registerForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); 
    registerUser(); 
  });

function registerUser() {
  const username = document.getElementById("username").value;
    const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ username, password }),
  })
    .then((response) => response.json())
    .then((data) => {
      const messageDiv = document.getElementById("message");
      if (data.success) {
        messageDiv.style.color = "green";
        const newLocal = "registered";
        console.log(newLocal);
        messageDiv.textContent = "Registration successful!";
      } else {
        messageDiv.textContent = data.message;
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}
