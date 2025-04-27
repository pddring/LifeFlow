let remainingTimeElement = document.querySelector("#title"),
         	 secondsLeft = 2

const downloadTimer = setInterval( 
    () => {
        if (secondsLeft <= 0)transitionToPage('emergency.html')
        remainingTimeElement.value = secondsLeft
        remainingTimeElement.textContent = "Emergency mode will enable in " + secondsLeft + "s";
        secondsLeft -= 1   
    }, 
1000)