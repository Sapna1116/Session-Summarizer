from moviepy.editor import VideoFileClip
from pytube import YouTube
from datetime import datetime
import os


def validate_video_link(video_link):
    """
    Validates the provided video link.

    Args:
        video_link (str): The video link to be validated.

    Returns:
        str or bool: Error message if the link is invalid, otherwise True.
    """
    if not video_link:
        return "!!!...No video link provided...!!!"
    
    # Check whether the provided input is a valid video source or not
    elif not ( video_link.startswith("http") or os.path.exists(video_link) ):
        return "!!!...Invalid input provided..!!! \nPlease provide a valid video link or file path..."

    return True


def extract_audio_from_video(src):
    """
    Extracts audio from a video source.

    Args:
        src (str): The source of the video (URL or local file path).

    Returns:
        AudioFileClip: Audio clip extracted from the video.
    """
    try:
        if isinstance(src, str) and src.startswith("http"):
            # If the source is a URL, use pytube to download the video
            video = YouTube(src)
            audio = video.streams.filter(only_audio=True).first()
        
        elif isinstance(src, str) and os.path.isfile(src):
            # If the source is a local file path, use moviepy to extract audio
            video = VideoFileClip(src)
            audio = video.audio
        else:
            # If the source is an UploadedFile object
            # Save the uploaded file to a temporary location
            with open("temp_video.mp4", "wb") as f:
                f.write(src.read())
            # Use moviepy to extract audio
            video = VideoFileClip("temp_video.mp4")
            audio = video.audio
            # Delete the temporary file
            os.remove("temp_video.mp4")
        
        return audio
    
    except Exception as e:
        print("An error occurred while extracting audio:", e)


def save_audio(video_link, audio, audio_file_path, current_dir):
    """
    Saves the audio to a file.

    Args:
        video_link (str): The video link or local file path.
        audio (AudioFileClip): Audio clip to be saved.
        audio_file_path (str): Path to save the audio file.
    """
    try:
        if isinstance(video_link, str) and video_link.startswith("http"):
            audio = audio.download(output_path = current_dir)
            os.replace(audio, audio_file_path)

        else : 
            audio.write_audiofile(audio_file_path, logger = None)
            
    except Exception as e:
        print("An error occurred while saving the audio:", e)




# If this script is called directly
if __name__ == "__main__":  

    # Get the directory of the current script
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define output file's location path 
    audio_file_path = os.path.join(CURRENT_DIRECTORY, f"converted_audio_{timestamp}.wav")

    # Get the Input Video from User
    input_video_link = input("\nEnter the Video Link/Path :- ").strip()
    

    # Check the validity of the source
    if validate_video_link(input_video_link) is not True:
        print(validate_video_link(video_link=input_video_link))
    else:
        # Convert Video
        print("\nConverting the video to audio...")
        audio = extract_audio_from_video(input_video_link)

        if audio is not None:
            # Save Audio
            print("Saving the Audio...")
            save_audio(input_video_link, audio, audio_file_path, CURRENT_DIRECTORY)
            print("The Audio is saved at :- ", audio_file_path)
        else : 
            print("Audio couldn't be loaded...")