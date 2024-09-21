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


