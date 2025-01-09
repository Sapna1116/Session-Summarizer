import streamlit as st
import backend

def get_response(video_source):
    transcript = backend.video_transcribe(video_source)
    response = backend.summarize_transcript(transcript)
    cost = backend.cost_analysis()
    return (transcript, response, cost)

# Streamlit UI elements
st.title("Meeting Summarization and Action-Items App")

# Create radio buttons for source selection
source_options = ["Choose the source type"] + ["Downloaded File", "Youtube URL"]
source = st.sidebar.selectbox("Pick the source:", source_options)

# Display the selected source
if source != "Choose the source type":
    st.sidebar.write(f"You selected {source}")

    uploaded_file = None
    url = None

    if source == "Downloaded File":
        uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "mov", "avi"])
    elif source == "Youtube URL":
        url = st.text_input("Enter Youtube URL")

    if uploaded_file or url :
        # If 'Summarize' button is clicked
        if st.button("Process"):
            
            video_src = uploaded_file if uploaded_file else url
            result = get_response(video_source=video_src)

            # Display Transcript
            st.subheader("Transcript of the Video")
            st.write(result[0])  # Display transcript

            st.subheader("Summary and Action-Items from the Video")
            st.subheader("Summary:")
            st.write(result[1]['summary'])
            st.subheader("Key Takeaways:")
            st.write(result[1]['key_takeaways'])
            st.subheader("Action Items Assigned:")
            st.write(result[1]['action_items'])

            st.subheader("Cost-Analysis Report of the process")
            st.write(result[2])  # Display cost-analysis report