async function detectEmotionImage() {
  const imageFile = document.getElementById("image-upload").files[0];

  // Check if a file was selected
  if (!imageFile) {
    alert("Please select an image file.");
    return;
  }

  // Prepare the FormData to send the file to the server
  const formData = new FormData();
  formData.append("file", imageFile);

  // Show loading message
  document.getElementById("image-result").innerHTML = "<p>Processing...</p>";

  try {
    // Send the image file to the backend API
    const response = await fetch("http://127.0.0.1:8000/detect_emotion_image/", {
      method: "POST",
      body: formData,
    });

    // Handle server response
    const data = await response.json();

    // Check if the response was successful
    if (response.ok) {
      if (data.status === "success" && data.emotions && data.emotions.faces.length > 0) {
        const face = data.emotions.faces[0];
        const dominantEmotion = face.dominant_emotion;
        const confidence = face.emotion[dominantEmotion];

        // Display the detected emotion and confidence
        document.getElementById("image-result").innerHTML = `
          <p><strong>Dominant Emotion:</strong> ${dominantEmotion}</p>
          <p><strong>Confidence:</strong> ${confidence.toFixed(2)}%</p>
        `;
      } else {
        document.getElementById("image-result").innerHTML = `
          <p>No emotion detected or error in response.</p>
        `;
      }
    } else {
      // Handle errors from the API response
      document.getElementById("image-result").innerHTML = `
        <p>Error: ${data.details || 'Unknown error from server'}</p>
      `;
    }
  } catch (error) {
    // Catch any fetch or network errors
    document.getElementById("image-result").innerHTML = `
      <p>Error: ${error.message}</p>
    `;
  }
}
