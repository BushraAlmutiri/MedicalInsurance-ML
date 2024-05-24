document.getElementById('firstForm').addEventListener('submit', function(event) {
  event.preventDefault();

  var email = document.getElementById('popup-input').value;

  fetch('http://127.0.0.1:8000/', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({
              email: email,
          }),
      })
      .then(response => response.json())
      .then(data => {
          console.log(data);
      })
      .catch((error) => {
          console.error('Error:', error);
      });
});









const popupElement = document.getElementById("popup");
const firstForm = document.getElementById("firstForm");
const predictionPage = "./pages/prediction.html";

//Events Listeners
firstForm.addEventListener("submit", (event) => {
  window.location.href = predictionPage;
  handleFormSubmit(event);
});
// the home pop up visibility
document.getElementById("start-btn").addEventListener("click", () => {
  popupElement.style.visibility = "visible";
});

function handleFormSubmit(event) {
  event.preventDefault(); // Prevent default form submission

  // Access form data using FormData object
  const formData = new FormData(event.target);
  for (const [key, value] of formData?.entries()) {
    console.log(`${key}: ${value}`);
  }
}

