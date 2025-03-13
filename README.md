# Triluxo_Technologies_intern_assignment



# Brainlox Chatbot

## Overview
This project is a Flask-based chatbot that retrieves information about technical courses from [Brainlox](https://brainlox.com). It uses web scraping, FAISS vector storage, and an LLM from Hugging Face to provide responses to user queries.

## Features
- Scrapes course information from Brainlox
- Splits text into meaningful chunks
- Converts text into embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- Stores embeddings in FAISS for fast retrieval
- Uses `tiiuae/falcon-7b-instruct` as the LLM for answering questions
- Provides a RESTful API with Flask

## Tech Stack
- **Flask**: API framework
- **LangChain**: For document loading, text splitting, retrieval, and LLM integration
- **Hugging Face**: For embeddings and LLM inference
- **FAISS**: For vector-based retrieval
- **Requests**: For making API calls

## Setup
### Prerequisites
Ensure you have Python 3.10+ installed.




Set up environment variables:   
   export USER_AGENT="Brainlox_chatbot/1.0"
   export HUGGINGFACEHUB_API_TOKEN="your_huggingface_api_key"
   




Run the Flask server:
   python3 app.py
   



## API Usage
### Endpoint: `/ask`
- **Method**: POST
- **Request Body** (JSON):
  
  { "query": "What is the cost of the course?" }
  
- **Response** (JSON):
  
  { "result": "The course costs $50." }
  





### Example Using Python `requests`

import requests

url = "http://127.0.0.1:5000/ask"
headers = {"Content-Type": "application/json"}
data = {"query": "explain about the course LEARN CLOUD COMPUTING BASICS-AWS"}

response = requests.post(url, json=data, headers=headers)
print(response.status_code)
print(response.json())


## Troubleshooting
- **Flask not running?** Ensure no other process is using port 5000:
  
  lsof -i :5000
  pkill -f flask


  Then restart the Flask app.
- **Connection issues?** Check internet connectivity or API key validity.





