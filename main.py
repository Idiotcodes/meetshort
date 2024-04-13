from flask import Flask, render_template, request, redirect, session
import os
from audio_to_text import audio_to_text  # Import audio_to_text function
from summarizer import text_summarizer
from keynote import generate_keynotes
from video_to_text import video_to_text

app = Flask(__name__)
app.secret_key = 'meetshort'  # Set a secret key for session management

ALLOWED_EXTENSIONS = {'wav'}  # Only allow WAV files


# Function to check allowed file extensions
def allowed_file(filename):
  return '.' in filename and filename.rsplit(
      '.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
  return render_template('index.html')


@app.route('/audioupload', methods=['GET', 'POST'])
def audioupload():
  if request.method == 'POST':
    file = request.files['file']  # Define file variable
    if file and allowed_file(file.filename):
      audio_path = os.path.join(app.static_folder, 'uploads', file.filename)
      file.save(audio_path)
      session['audio_filename'] = file.filename  # Store filename for later use
      return redirect(
          '/generate_transcript')  # Redirect to generate_transcript route
  return render_template('audioupload.html')


@app.route('/generate_transcript', methods=['POST'])
def generate_transcript():
  file = request.files['file']  # Define file variable
  if file.filename == '':
    return "No selected file"
  if file and allowed_file(file.filename):
    audio_path = os.path.join(app.static_folder, 'uploads', file.filename)
    file.save(audio_path)
    output_dir = os.path.join(app.static_folder, 'output')
    transcription = audio_to_text(audio_path, output_dir=output_dir)
    if transcription:
      session[
          'transcription_generated'] = True  # Flag to indicate transcription exists
      return redirect('/audiotranscript')
    else:
      return "Error processing audio"
  else:
    return "Invalid file type."


@app.route('/audiotranscript')
def audiotranscript():
  transcript_path = os.path.join(app.static_folder, 'output', 'transcript.txt')
  summary_path = os.path.join(app.static_folder, 'output', 'summary.txt')
  keynote_path = os.path.join(app.static_folder, 'output', 'keynotes.txt')
  output_dir = os.path.join('static', 'output')
  text_summarizer(transcript_path, output_dir)
  generate_keynotes(transcript_path)
  try:
    with open(transcript_path, 'r') as f:
      transcript = f.read()
    try:
      with open(summary_path, 'r') as f:
        summary = f.read()
    except FileNotFoundError:
      summary = "Summary not found. Please generate a summary."
  except FileNotFoundError:
    transcript = "Transcript not found. Please generate a transcript."
    summary = "Summary not found. Please generate a summary."
  try:
    with open(keynote_path, 'r') as f:
      keynote = f.read()
  except FileNotFoundError:
    keynote = "Keynotes not found. Please generate keynotes."

  return render_template('audiotranscript.html',
                         transcript=transcript,
                         summary=summary,
                         keynote=keynote)


@app.route('/videoupload', methods=['GET', 'POST'])
def videoupload():
  if request.method == 'POST':
    file = request.files['file']
    if file:
      video_path = os.path.join(app.static_folder, 'uploads', file.filename)
      file.save(video_path)
      session['video_filename'] = file.filename  # Store filename for later use
      return redirect('/generate_video_transcript')
  return render_template(
      'videoupload.html')  # Create a new template for video upload


@app.route('/generate_video_transcript', methods=['POST'])
def generate_video_transcript():
  video_filename = session.get('video_filename')
  if not video_filename:
    return "No video uploaded."

  video_path = os.path.join(app.static_folder, 'uploads', video_filename)
  output_dir = os.path.join(app.static_folder, 'output')
  transcription = video_to_text(video_path, output_dir)

  if transcription:
    session['transcription_generated'] = True
    return redirect(
        '/audiotranscript')  # Reuse the existing audiotranscript route
  else:
    return "Error processing video"


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000)
