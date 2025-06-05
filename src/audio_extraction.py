
import imageio_ffmpeg as ffmpeg
import subprocess
import os

def extract_audio(video_path: str, output_audio_path: str):
    try:
        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

        ffmpeg_path = ffmpeg.get_ffmpeg_exe()  # Get bundled ffmpeg binary

        command = [
            ffmpeg_path,
            "-y",
            "-i", video_path,
            "-vn",
            "-acodec", "mp3",
            output_audio_path
        ]
        subprocess.run(command, check=True)
        print(f"Audio extracted to {output_audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg error: {e}")
    except Exception as e:
        print(f"Error extracting audio: {e}")
