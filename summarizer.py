import requests
import os
from dotenv import load_dotenv

load_dotenv()


def text_summarizer(transcript_path, output_dir="static/output"):
  hug_api_key = os.environ.get("HUG_API_KEY")
  if not hug_api_key:
    print("Hugging Face API key not found.")
    return None

  with open(transcript_path, "r") as file:
    transcript_text = file.read()

  url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
  headers = {"Authorization": f"Bearer {hug_api_key}"}
  try:
    response = requests.post(url, headers=headers, json=transcript_text)
    response.raise_for_status()
    if response.status_code == 200:
      summarized_text_list = response.json()

      # Convert dictionaries to strings
      summarized_text_list = [
          item["summary_text"] for item in summarized_text_list
      ]

      summarized_text = "\n".join(summarized_text_list)

      os.makedirs(output_dir, exist_ok=True)
      summary_filename = "summary.txt"
      summary_path = os.path.join(output_dir, summary_filename)

      with open(summary_path, "w") as f:
        f.write(summarized_text)

      return summarized_text
    else:
      print(f"Error: {response.status_code}")
      return None
  except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
    return None
