# Text-To-Speech-Using-OpenAI
Simple yet powerful FastAPI-based application for converting text into speech using OpenAI's speech synthesis capabilities. Designed for developers looking to integrate text-to-speech functionality into their projects

Key Features:
FastAPI Framework: Built using FastAPI, this application provides a fast and efficient API for text-to-speech conversion, with easy-to-understand endpoints and robust error handling.
OpenAI Integration: Utilizes OpenAI’s speech synthesis model to create lifelike voice outputs, allowing users to convert text into clear and natural-sounding speech.
Easy-to-Use API Endpoint: Includes a single endpoint /convert-to-speech/ where users can submit text via a POST request and receive an audio file in response.
Customizable Output: Allows for easy modification of parameters such as voice selection and model choice, making it flexible for different use cases.
Error Handling: Equipped with comprehensive error handling, including HTTP exceptions to ensure graceful handling of any issues during the speech synthesis process.

How It Works:
Input Text: Users send a POST request to the /convert-to-speech/ endpoint with the text they want to convert to speech.
Audio Generation: The application uses the OpenAI API to generate speech from the text input, utilizing the specified model and voice settings.
File Delivery: The generated speech is saved as an MP3 file and returned to the user as a downloadable response.

Setup and Usage:
Clone the repository.
Set up the environment variables, including the OPENAI_API_KEY.
Run the FastAPI application using uvicorn.
Send requests to the /convert-to-speech/ endpoint to convert text into speech.
This application is ideal for developers needing a quick and reliable solution for text-to-speech conversion, making it a valuable addition to any voice-enabled project.

#Code
#######

from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()


api_key = os.getenv("OPENAI_API_KEY", "Insert_key_here")
client = OpenAI(api_key=api_key)

# Base directory to save the audio file
BASE_DIR = Path(__file__).parent

# Define the request model
class TextToSpeechRequest(BaseModel):
    text: str

@app.post("/convert-to-speech/")
async def convert_to_speech(request: TextToSpeechRequest):
    try:
        # Extract the text from the request model
        text = request.text
        
        # Set the path for the output speech file
        speech_file_path = BASE_DIR / "speech.mp3"
        
        # Create the speech using the OpenAI client
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=text
        )

        # Save the speech to the file
        response.stream_to_file(speech_file_path)

        return FileResponse(speech_file_path, media_type="audio/mpeg", filename="speech.mp3")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
