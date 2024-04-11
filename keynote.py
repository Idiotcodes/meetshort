import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Load API keys
load_dotenv()
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")


# Function to generate keynotes
def generate_keynotes(transcript_path, output_dir="static/output"):

  # Initialize Gemini-Pro model
  try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",  # Specify Gemini-Pro
        google_api_key=GOOGLE_API_KEY,
        max_output_tokens=100)
  except ValueError as e:
    print(f"Error initializing Gemini model: {e}")
    return None

  # Read transcript
  try:
    with open(transcript_path, "r") as file:
      transcript = file.read()
  except FileNotFoundError as e:
    print(f"Error reading transcript file: {e}")
    return None

  # Generate keynotes
  message = HumanMessage(
      content=
      f"Generate keynotes from the following transcript, also don't use any beautifers like bold, italics, underscore, etc. Keep it plain text:\n\n{transcript}"
  )
  try:
    response = llm.invoke([message])
    keynotes = response.content
  except Exception as e:
    print(f"Error generating keynotes: {e}")
    return None

  # Write keynotes to a file
  os.makedirs(output_dir, exist_ok=True)
  keynotes_filename = "keynotes.txt"
  keynotes_path = os.path.join(output_dir, keynotes_filename)
  try:
    with open(keynotes_path, "w") as f:
      f.write(keynotes)
  except OSError as e:
    print(f"Error writing keynotes to file: {e}")
    return None

  return keynotes
