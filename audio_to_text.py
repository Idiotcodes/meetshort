import requests
import os
from dotenv import load_dotenv

load_dotenv()


def audio_to_text(audio_path, output_dir="static/output"):
  hug_api_key = os.environ.get("HUG_API_KEY")
  if not hug_api_key:
    print("Hugging Face API key not found.")
    return None

  url = "https://api-inference.huggingface.co/models/openai/whisper-large-v3"
  headers = {"Authorization": f"Bearer {hug_api_key}"}
  files = {"audio": open(audio_path, "rb")}

  try:
    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    if response.status_code == 200:
      transcription = response.json().get("text")

      os.makedirs(output_dir, exist_ok=True)
      transcript_filename = "transcript.txt"
      transcript_path = os.path.join(output_dir, transcript_filename)

      with open(transcript_path, "w") as f:
        f.write(transcription)

      return transcription
    else:
      print(f"Error: {response.status_code}")
      return None
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None
