import os
from moviepy.editor import VideoFileClip
from audio_to_text import audio_to_text  # Import audio_to_text function


def extract_audio(video_path, output_dir="static/uploads"):
  # Extract audio from video and save it as WAV file
  audio_filename = os.path.splitext(os.path.basename(video_path))[0] + ".wav"
  audio_path = os.path.join(output_dir, audio_filename)

  video = VideoFileClip(video_path)
  audio = video.audio
  audio.write_audiofile(audio_path, codec='pcm_s16le',
                        bitrate='8k')  # Set bitrate to a very low value

  return audio_path


def video_to_text(video_path, output_dir="static/output"):
  # Extract audio from video
  audio_path = extract_audio(video_path)

  # Call audio_to_text function
  return audio_to_text(audio_path, output_dir)


if __name__ == "__main__":
  # Example usage
  video_path = "video.mp4"  # Replace with the path to your video file
  app = None  # Replace with your Flask app instance
  transcription = video_to_text(video_path, app)
  print(transcription)
