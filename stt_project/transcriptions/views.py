from django.shortcuts import render
from django import forms
from openai import OpenAI
import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

os.getenv("OPENAI_API_KEY")
class UploadFileForm(forms.Form):
    audio_file = forms.FileField()

def index(request):
    context = None
    print("Path", request.path)
    print("Path", request.get_host())
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {"error": "Provide a valid file"}
            return render(request, "transcriptions/index.html", context)

        try:
            # Get file
            file = request.FILES['audio_file']

            # Save the file temporarily
            temp_file_path = "temp_audio_file.mp3"
            with open(temp_file_path, "wb+") as temp_file:
                for chunk in file.chunks():
                    temp_file.write(chunk)

            # Transcribe with OpenAI's Whisper model
            with open(temp_file_path, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )

            # Delete the temporary file
            os.remove(temp_file_path)

            # Return transcript or error
            context = {"transcript": transcript.text}
        except Exception as e:
            context = {"error": str(e)}

    return render(request, "transcriptions/index.html", context)