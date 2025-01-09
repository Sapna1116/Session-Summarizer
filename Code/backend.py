import audio_extraction
import transcription
import required_responses
from datetime import datetime
import os


# Get the directory of the current script
CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Generate timestamp
TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def video_transcribe(video_source, current_dir_path = CURRENT_DIRECTORY):
    """
    Convert the video with the source as a link to audio.

    Args:
        video_source(str): The link or path to the video.

    Returns:
        tuple: Tuple containing the audio data and the path to the saved audio file.
    """
    # No need to check the validity of the source

    print("\nConverting the video to audio...")
    audio = audio_extraction.extract_audio_from_video(src=video_source)
    print("Saving the Audio...")
    audio_file_path = os.path.join(current_dir_path, f"converted-audio_{TIMESTAMP}.wav")
    audio_extraction.save_audio(video_source, audio, audio_file_path, current_dir_path)
    print("The Audio is saved at :- ", audio_file_path)
    
    print("\nGenerating the Transcript from the audio...")
    transcript = transcription.transcribe_audio(audio_path=audio_file_path)
    return transcript

def summarize_transcript(transcript):
    """
    Generate summary and action-items from the transcript.

    Args:
        transcript (str): The transcript text.

    Returns:
        dict: A dictionary containing the summary and action-items.
    """
    print("\nGenerating summary and drawing conclusions...")
    response = required_responses.generate_summary(transcript=transcript)
    return response

def cost_analysis():
    """
    Get the cost-analysis report.
    """
    print("\nCost-Analysis report ...")
    response_cost = required_responses.calculate_response_cost()

    return response_cost

    

if __name__ == "__main__" :
    
    try:
        # Get the directory of the current script
        UPDATED_CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__)) + "/Results/"
        if not os.path.exists(UPDATED_CURRENT_DIRECTORY):
            os.makedirs(UPDATED_CURRENT_DIRECTORY)
            
        
        # Get the Input Video from User
        video_link = input("\nEnter the Video Link/Path :- ").strip()
        
        # Check the validity of the source
        if audio_extraction.validate_video_link(video_link) is not True:
            print(audio_extraction.validate_video_link(video_link=video_link))
        
        # If the video source is valid
        else:

            # --------------------------------------------------------------------------------------------------
            # STEP-1  ->  Video-To-Transcription
            # --------------------------------------------------------------------------------------------------

            try:
                # Transcribe the video
                transcript = video_transcribe(video_source=video_link, current_dir_path=UPDATED_CURRENT_DIRECTORY)
                
                # Save the Transcription
                print("Saving the Transcript...")
                transcript_file_path = os.path.join(UPDATED_CURRENT_DIRECTORY, f"transcripted-text_{TIMESTAMP}.txt")
                transcription.save_transcript(transcript, transcript_file_path)
                print("The Transcription is saved at :- ", transcript_file_path)

                # --------------------------------------------------------------------------------------------------
                # STEP-2  ->  Transcription-To-Summary-&-Action-Items
                # --------------------------------------------------------------------------------------------------

                try:
                    # Summarize the Audio content
                    response = summarize_transcript(transcript)

                    # Save the summary & action-items assigned
                    print("Saving the Summary and the Action-Items Assigned...")
                    result_file_path = os.path.join(UPDATED_CURRENT_DIRECTORY, f"result_text_{TIMESTAMP}.txt")
                    required_responses.save_result(response, result_file_path)
                    print("The Summary is saved at:", result_file_path)


                    # --------------------------------------------------------------------------------------------------
                    # STEP-3  ->  Generate Transcript's Cost-Analysis Report
                    # --------------------------------------------------------------------------------------------------

                    try:
                        # (A) Save the Cost-Analysis Report
                        response_cost_path = os.path.join(UPDATED_CURRENT_DIRECTORY, f"response_cost_text_{TIMESTAMP}.txt")
                        
                        response_cost = cost_analysis()
                        
                        print("\nSaving Cost-Analysis report ...")
                        required_responses.save_response_cost(response_cost, response_cost_path)
                    
                        print("The Cost-Analysis report is saved at:", response_cost_path)
                    
                    except Exception as e:
                        print("Error occurred while saving Cost-Analysis report:", e)
                
                except Exception as e:
                    print("Error occurred during step 2:", e)

            except Exception as e:
                print("Error occurred during step 1:", e)
    
    except Exception as e:
        print("Error occurred:", e)
