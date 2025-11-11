from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import requests
from io import BytesIO

# FastAPI app initialization
app = FastAPI(
    title="Emotion Detection API",
    description="Detect emotions from images using Luxand API.",
    version="1.0.0"
)

# -------------------- CONFIG --------------------
# Luxand Emotion Recognition API (Image)
LUXAND_API_KEY = "64b3b4c749214189957ceeef18155dbe"
LUXAND_API_URL = "https://api.luxand.cloud/photo/emotions"

# -------------------- CORS CONFIGURATION --------------------
origins = [
    "http://127.0.0.1",  # Frontend running locally
    "http://localhost",  # Another common localhost URL
    "http://localhost:8000",  # For testing on the same machine with different ports
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Emotion Detection API! Use /docs to explore the endpoints."}

@app.post("/detect_emotion_image/")
async def detect_emotion_image(file: UploadFile = File(...)):
    """
    Detects emotion from an uploaded image file using the Luxand API.
    """
    try:
        # Read the uploaded image
        image_data = await file.read()

        # Luxand requires token-based header authentication
        headers = {
            "token": LUXAND_API_KEY
        }
        files = {
            "photo": ("image.jpg", image_data, file.content_type)
        }

        # Send request to Luxand API
        response = requests.post(LUXAND_API_URL, headers=headers, files=files)

        # Parse and return result
        if response.status_code == 200:
            emotion_data = response.json()
            return {
                "status": "success",
                "service": "Luxand Cloud",
                "emotions": emotion_data
            }
        else:
            return {
                "status": "error",
                "code": response.status_code,
                "details": response.text
            }
    except Exception as e:
        # Log the error message for debugging
        print(f"Error: {str(e)}")
        return {"error": str(e)}
