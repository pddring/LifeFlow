eel.emergency();
console.log('emergency mode activated')

// Fetch the JSON file to retrieve the ID
fetch('../../settings.json')
  .then(response => response.json())
  .then(data => {
    // Retrieve the 'hub' value from the JSON
    const ID = data.hub;

    // Construct the URL with the retrieved ID
    const url = "http://localhost/api/fall_detected.php?badge_id=" + ID;

    // Send a GET request to the constructed URL
    fetch(url)
      .then(response => {
        if (response.ok) {
          console.log('Request successful');
        } else {
          console.error('Request failed with status:', response.status);
        }
      })
      .catch(error => {
        console.error('Error with the request:', error);
      });
  })
  .catch(error => {
    console.error('Error fetching JSON:', error);
  });
