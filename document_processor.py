import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import openai
import time
from langchain import OpenAI


from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY1")
llm = OpenAI(temperature=0,
             model="gpt-3.5-turbo-16k-0613",
             openai_api_key=openai_api_key
            )

# Set OpenAI API key
openai.api_key = openai_api_key
# Configuration
CHUNK_SIZE = 16384
CHUNK_OVERLAP = 512
DATA_FOLDER = 'data'

def chunk_document(doc, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '\t'],
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    chunks = text_splitter.split_text(doc)
    return chunks

# def process_file(file_path):
#     with open(file_path, 'r') as f:
#         text = f.read()

#     chunks = chunk_document(text)
#     return chunks

def process_file(file_path):
    """
    Read and process a file, assuming it's a text file.
    
    Parameters:
    - file_path (str): Path to the file to be processed.
    
    Returns:
    - str: Contents of the file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except UnicodeDecodeError:
        # Handle encoding errors gracefully by trying a different encoding
        with open(file_path, 'r', encoding='latin-1') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        text = ""
    
    chunks = chunk_document(text)
    return chunks


def summarize_chunks(chunks):
    print(openai_api_key)
    from openai import OpenAI
    client = OpenAI(api_key=openai_api_key)

    summaries = {}
    for i, chunk in enumerate(chunks):
        prompt = f"Write a concise and verbose summary of the following text along with examples that would make someone understand even if they are 12 year old.  It should be concise and verbose and should cover the key points and intent of the text.\n\n{chunk}"
        
        response = client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': "You are expert in document summary"},
                {'role': 'user', 'content': prompt}
                ],
                model="gpt-3.5-turbo-0125",
                temperature=0.1,
                # response_format={"type": "json_object"},
                )
        summaries[f"Node_{i+1}_summary"] = response.choices[0].message.content.strip()
    return summaries

def generate_final_response(summaries):
    from openai import OpenAI
    client = OpenAI(api_key=openai_api_key)

    prompt = f"You will be provided with summaries sepated by two new lines. Your job is to create a main summary which is concise and verbose that completely captures the intent verbosely. It should cover the key points and intent of the text.\n\n{summaries}"
        
    response = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': "You are expert in document summary"},
            {'role': 'user', 'content': prompt}
            ],
            model="gpt-3.5-turbo-0125",
            temperature=0.1,
            # response_format={"type": "json_object"},
            )
    response = response.choices[0].message.content.strip()
    return response