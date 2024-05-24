window.onload = function () {
  document
    .getElementById("contactForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      // Get form input values
    const name = document.getElementById("from_name").value.trim();
    const email = document.getElementById("email").value.trim();
    const message = document.getElementById("message").value.trim();

    // Check if required fields are filled
    if (name === '' || email === '' || message === '') {
      alert("Please fill in all required fields.");
      return;
    }

    emailjs.send( "service_mxfp4cp", "template_f5vo1kb",{
      from_name: name,
      email: email,
      message: message
    })


    .then(function(response) {
      console.log('Email sent successfully:', response);
      alert("Your message has been sent successfully!");
      // Clear form inputs after successful submission
      document.getElementById("from_name").value = '';
      document.getElementById("email").value = '';
      document.getElementById("message").value = '';
    }, function(error) {
      console.error('Email send failed:', error);
      alert("There was an error sending your message. Please try again later.");
    });
  });
};