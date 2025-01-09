### OVERVIEW

This project aims to develop a tool for meeting summarization and analysis. The project is divided into several modules, each responsible for a specific task, and it utilizes various Python libraries to achieve its objectives.


### MODULES

1. audio_extraction.py
This module is responsible for converting received meeting videos into audio format. It utilizes different Python libraries based on the source of the video:
moviepy for downloaded files
pytube for videos available on YouTube.

2. transcription.py
This module performs the transcription of the audio generated in the previous step.

3. required_responses.py
This module retrieves the required outputs from the transcript using prompts. It includes:-
- Summary
- Key takeaways
- Assigned tasks
Additionally, it retrieves the cost-analysis report for the OpenAI LLM call using the Langchain OpenAICallbackHandler.

4. backend.py
The backend.py module orchestrates the execution of the three unit modules: audio_extraction.py, transcription.py, and required_responses.py.

5. frontend.py
The frontend.py module creates a user interface using Python's Streamlit framework. It allows users to select and choose the type of video source. Upon selecting the "Process" option, it triggers the execution of the backend modules to generate the required outputs.


### USAGE

To utilize the tool:
- Ensure you have Python installed on your system.
- Install the required Python libraries specified in the respective modules.
- Run the frontend.py module to access the user interface.
- Select the video source type and follow the prompts.
- Upon selecting "Process," the tool will generate the required outputs.

### SECURITY

The OpenAPI authentication key is securely stored in a separate file to ensure data confidentiality and security.


