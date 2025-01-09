import whisper
import warnings
from datetime import datetime
import os


def validate_audio_link(audio_path):
    """
    Validates the provided audio link.

    Args:
        audio_path (str): The audio link to be validated.

    Returns:
        str or bool: Error message if the link is invalid, otherwise True.
    """
    if not audio_path:
        return "!!!...No audio path provided...!!!"
    
    # Check whether the provided input is a valid video source or not
    elif not os.path.exists(audio_path) :
        return "!!!...Invalid input provided..!!! \nPlease provide a valid audio file path..."

    return True


def transcribe_audio(audio_path):
    """
    Transcribes the audio file using the Whisper library.

    Args:
        audio_path (str): The path to the audio file.

    Returns:
        str: The transcribed text.
    """
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
    except Exception as e:
        return f"Transcription failed: {e}"


def save_transcript(transcript, transcript_file_path):
    """
    Saves the transcript to a text file.

    Args:
        transcript (str): The transcript text.
        transcript_file_path (str): The path to save the transcript file.
    """
    try:
        with open(transcript_file_path, "w") as f:
            f.write(transcript)
        return True
    except Exception as e:
        return f"Saving transcript failed: {e}"



# If this script is called directly
if __name__ == "__main__":

    # Suppress the specific UserWarning
    warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

    # Get the directory of the current script
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define output file's location path 
    transcript_file_path = os.path.join(CURRENT_DIRECTORY, f"transcripted_text_{timestamp}.txt")

    # Get the Audio File Path from the User
    input_audio_path = input("\nEnter the Audio Path :- ").strip()
    

    # Check the validity of the source
    validation_result = validate_audio_link(input_audio_path)
    if validation_result is not True:
        print(validation_result)
    else:
        # Transcribe audio
        transcribed_text = transcribe_audio(input_audio_path)
        if isinstance(transcribed_text, str):
            # Save transcript
            print("Saving the Transcript...")
            save_result = save_transcript(transcribed_text, transcript_file_path)
            if save_result is True:
                print("The Transcription is saved at:", transcript_file_path)
            else:
                print("Error:", save_result)
        else:
            print("Error:", transcribed_text)