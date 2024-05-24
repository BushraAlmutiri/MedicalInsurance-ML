const predictionForm = document.getElementById("predictionForm");
const result = document.getElementById("result");
const amount = document.querySelectorAll("span");
let welcomeName = document.getElementById("name");
const prophesyBtn = document.getElementById("prophesyCost");

predictionForm.addEventListener("submit", (event) => {
  event.preventDefault(); // Prevent the default form submission behavior
  resultVisibility();
  handleFormSubmit(event);
});

// Function to update the name
function updateName(newName) {
  currName = newName; // Update the current name
  welcomeName.innerText = currName; // Update the displayed name
}


function resultVisibility() {
  result.style.display = "flex"; // Make sure 'result' is the ID of your result container
  prophesyBtn.style.display = "none";
}

// Function to fetch predictions from the server using Axios
function fetchPredictions() {
  axios.get("http://127.0.0.1:8000/", {
      headers: {
          "Content-Type": "application/json"
      }
  })

  .then(response => {
      console.log(response.data);
      // Handle data here e.g., display it in the DOM
  })
  .catch(error => console.error('Error:', error));
}

// Function to handle the form submission using Axios
function handleFormSubmit(event) {
  event.preventDefault();
  const data = {
    children: document.getElementById("children").value,
    age: document.getElementById("age").value,
    sex: parseInt(document.querySelector('input[name="sex"]:checked').value),
    bmi: document.getElementById("Bmi").value,
    region: parseInt(document.getElementById("region").value),
    smoker: parseInt(document.querySelector('input[name="smoker"]:checked').value),
  };

  axios.post("http://127.0.0.1:8000/predict", data, {
    headers: {
      "Content-Type": "application/json",
    }
  })
  .then(response => {
    console.log(response.data);
    // Update the DOM with the prediction
    document.getElementById("predictionResult").innerText = `$ ${response.data.best_prediction}`;
    resultVisibility();
    document.getElementById("predictionResult2").innerText = `$ ${response.data.best_prediction} `;
     resultVisibility();
     document.getElementById("predictionResult3").innerText = ` ${response.data.best_model} model`;
     resultVisibility();
  })
  .catch(error => console.error('Error:', error.response ? error.response.data : error.message));
}
