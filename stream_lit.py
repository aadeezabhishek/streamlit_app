# import streamlit as st
# import time
# import os
# from document_processor import process_file, summarize_chunks, generate_final_response
# from dotenv import load_dotenv

# load_dotenv()

# # Streamlit settings
# st.set_page_config(page_title="File Upload and Summary Generation")

# # Title of the app
# st.title("Upload File and Generate Summary")

# # File uploader
# uploaded_file = st.file_uploader("Choose a file", type=["txt"])

# # Progress bar
# progress_bar = st.progress(0)
# progress_text = st.empty()

# def update_progress(progress, text):
#     progress_bar.progress(progress)
#     progress_text.text(text)

# if uploaded_file is not None:
#     # Save the uploaded file
#     file_path = os.path.join("uploads", uploaded_file.name)
#     with open(file_path, "wb") as f:
#         f.write(uploaded_file.getbuffer())

#     st.success("File uploaded successfully!")

# if st.button("Generate Summary") and uploaded_file is not None:
#     # Update progress and simulate delay for processing
#     update_progress(10, "File uploaded. Starting processing...")
#     time.sleep(2)  # Simulate delay for chunking

#     # Process the uploaded file
#     chunks = process_file(file_path)
#     update_progress(30, "File chunked. Starting summary generation...")

#     # Summarize chunks
#     summaries = summarize_chunks(chunks)
#     update_progress(60, "Summaries generated. Creating final response...")

#     # Combine all summaries into a single string
#     combined_summary = "\n\n".join(summaries.values())

#     # Create final summary
#     response = generate_final_response(combined_summary)
#     update_progress(100, "Processing complete.")

#     # Display the final summary
#     st.subheader("Generated Summary")
#     st.write(response)


import streamlit as st
import time
import os
from document_processor import process_file, summarize_chunks, generate_final_response
from dotenv import load_dotenv

load_dotenv()

# Streamlit settings
st.set_page_config(page_title="File Upload and Summary Generation")

# Title of the app
st.title("Upload File and Generate Summary")

# File uploader
uploaded_file = st.file_uploader("Choose a file", type=["txt"])

# Progress bar
progress_bar = st.progress(0)
progress_text = st.empty()

def update_progress(progress, text):
    progress_bar.progress(progress)
    progress_text.text(text)

if uploaded_file is not None:
    # Save the uploaded file
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("File uploaded successfully!")

if st.button("Generate Summary") and uploaded_file is not None:
    with st.spinner("Generating summary..."):
        # Update progress and simulate delay for processing
        update_progress(10, "File uploaded. Starting processing...")
        time.sleep(2)  # Simulate delay for chunking

        # Process the uploaded file
        chunks = process_file(file_path)
        update_progress(30, "File chunked. Starting summary generation...")

        # Summarize chunks
        summaries = summarize_chunks(chunks)
        update_progress(60, "Summaries generated. Creating final response...")

        # Combine all summaries into a single string
        combined_summary = "\n\n".join(summaries.values())

        # Create final summary
        response = generate_final_response(combined_summary)
        update_progress(100, "Processing complete.")

    # Display the final summary
    st.subheader("Generated Summary")
    st.write(response)
