from langchain_openai.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.openai_info import OpenAICallbackHandler
from secret_key import openai_key
from datetime import datetime
import re
import os

os.environ['OPENAI_API_KEY'] = openai_key

llm = OpenAI(temperature=0.9, callbacks=[OpenAICallbackHandler()])


def validate_transcript_link(transcript_path):
    """
    Validates the provided transcript link.

    Args:
        transcript_path (str): The transcript link to be validated.

    Returns:
        str or bool: Error message if the link is invalid, otherwise True.
    """
    if not transcript_path:
        return "!!!...No transcript path provided...!!!"
    
    # Check whether the provided input is a valid video source or not
    elif not os.path.exists(transcript_path):
        return "!!!...Invalid input provided..!!! \nPlease provide a valid transcript file path..."

    return True


def generate_summary(transcript):
    """
    Generate summary and conclusion from the transcripted text.

    Args:
        transcript_text (str): The transcripted text.

    Returns:
        dict: A dictionary containing the summary and key takeaways.
            Keys:
            - 'summary': The summary text.
            - 'key_takeaways': The key takeaways text.
            - 'action_items': The action-items assigned text.
    """
    try:
        # Chain 1: Generate Summary
        summary_prompt = PromptTemplate(
            input_variables=['transcript_text'],
            template = "Utilizing your proficiency in summarizing information, your task is to generate a detailed summary of the following text:- {transcript_text}, broken down into distinct paragraphs. Each paragraph should encapsulate a different aspect or theme of the conversation, ensuring a comprehensive overview."
        )

        # Chain 2: Generate Key-Takeaways
        key_takeaway_prompt = PromptTemplate(
            input_variables=['transcript_text'],
            template="Drawing upon your ability to distill information, your task is to extract and list the key takeaway points from the following text:- {transcript_text}. These points should encapsulate the most important ideas, findings, or topics discussed, providing a clear and succinct overview of the essence of the conversation."
        )

        # Chain 3 : Generate assigned Action-Items 
        action_item_prompt = PromptTemplate(
            input_variables=['transcript_text'],
            template="Your expertise lies in extracting action items by analyzing conversations. Please review the text below and identify any tasks, assignments, or actions discussed, along with the individuals responsible. List them in a concise format as 'Name : Task/Action Assigned'."
        )


        # Define Chains
        chain1 = LLMChain(llm=llm, prompt=summary_prompt, output_key="summary")
        chain2 = LLMChain(llm=llm, prompt=key_takeaway_prompt, output_key="key_takeaways")
        chain3 = LLMChain(llm=llm, prompt=action_item_prompt, output_key="action_items")

        # Invoke each chain separately
        try:
            response1 = chain1.invoke(input={'transcript_text': transcript})
        except Exception as e:
            print("Error in generating summary:", e)
            response1 = {'summary': 'Error in generating summary'}

        try:
            response2 = chain2.invoke(input={'transcript_text': transcript})
        except Exception as e:
            print("Error in generating key takeaways:", e)
            response2 = {'key_takeaways': 'Error in generating key-takeaways'}

        try:
            response3 = chain3.invoke(input={'transcript_text': transcript})
        except Exception as e:
            print("Error in generating action items:", e)
            response3 = {'action_items': 'Error in generating action-items'}


        # Combine responses into a single dictionary
        response = {
            'summary': response1['summary'],
            'key_takeaways': response2['key_takeaways'],
            'action_items' : response3['action_items']
        }

        # Return the result in the form of dictionary
        return response
    
    except Exception as e:
        print(f"An error occurred while generating the summary: {e}")
        return None     


def save_result(response, result_file_path):
    """
    Save the response

    Args:
        response (dict): A dictionary containing the summary, key-takeaways and action-items .
            It should have the following keys:
            - 'summary': The summary text.
            - 'key_takeaways': The key takeaways text.
            - 'action_items' : The action-items assigned text.
        result_file_path (str): The path to save the summary file.
    """
    try:
        with open(result_file_path, "w") as f:
            f.write("\n\nSummary:")
            f.write(response.get('summary', ''))
            f.write("\n\n\nKey Takeaways:")
            f.write(response.get('key_takeaways', ''))
            f.write("\n\n\nAction-Items Assigned:")
            f.write(response.get('action_items', ''))

    except Exception as e:
        print(f"An error occurred while saving the result: {e}")


def calculate_response_cost():
    response_cost = (str(llm.callbacks)).strip('[]')

    # Use regular expression to insert newline before non-digit characters except the decimal point
    response_cost = re.sub(r'(\d)([^0-9.])', r'\1\n\2', response_cost)
    # Remove leading spaces from each line
    response_cost = "\n".join(line.lstrip() for line in response_cost.split("\n"))
    
    return response_cost


def save_response_cost(response_cost, response_cost_path):
    """
    Saves the cost-analysis, for the response received, to a text file.

    Args:
        response_cost (str): The cost of responses received with each prompt call.
        response_cost_path (str): The path to save the transcript file.
    """
    try: 
        with open(response_cost_path, "w") as f:
            f.write(response_cost)

    except Exception as e:
        print(f"An error occurred while saving the result: {e}")


# If this script is called directly
if __name__ == "__main__":

    # Get the directory of the current script
    CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # Define output file's location path 
    result_file_path = os.path.join(CURRENT_DIRECTORY, f"result_text_{timestamp}.txt")
    # Define action-items file's location path 
    response_cost_path = os.path.join(CURRENT_DIRECTORY, f"cost_response_text_{timestamp}.txt")


    # Get the input transcript file path from the user
    input_transcript_path = input("\nEnter the transcripted file's path :- ").strip()
    # input_transcript_path =  "/home/sapna.choudhary/PYTHON/POC/transcripted-text_2024-04-24_09-35-19.txt"

    # Check the validity of the source
    validation_result = validate_transcript_link(transcript_path=input_transcript_path)
    if validation_result is not True:
        print(validation_result)
        
    else:

        # Read the content of the transcript file
        with open(input_transcript_path, "r") as file:
            transcript_text = file.read()

        # Generate Summary
        print("\nGenerating summary and drawing conclusions...")
        response = generate_summary(transcript = transcript_text)  
        
        # Save the summary & action-items
        print("Saving the Summary and the Action-Items Assigned...")
        save_result(response, result_file_path)
        print("The Summary is saved at:", result_file_path)

        # Cost-Analysis Report
        print("Saving Cost-Analysis report ...")
        response_cost = calculate_response_cost()
        save_response_cost(response_cost, response_cost_path)
        print("The Summary is saved at:", response_cost_path)