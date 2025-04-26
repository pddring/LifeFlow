const messages = [
    "Bienvenido",
    "Bienvenue",
    "Velkommen",
    "Willkommen",
    "Welcome"
  ];

  let currentIndex = 0;
  const messageElement = document.getElementById("message");

  function cycleMessages() {
    messageElement.classList.remove("fade-in-out");
    setTimeout(() => {
      messageElement.textContent = messages[currentIndex];
      void messageElement.offsetWidth; // Trigger reflow for the animation to work
      messageElement.classList.add("fade-in-out");
      currentIndex = (currentIndex + 1) % messages.length;
    }, 3000); // Set timeout to match the animation duration
  }

  // Change message every 5 seconds (5000 milliseconds)
  setInterval(cycleMessages, 2500);