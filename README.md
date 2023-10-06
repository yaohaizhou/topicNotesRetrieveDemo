# Introduction
This repo is a demo to retrieve topic notes (background knowledge) for AP calculus question.

# Run this demo
Fill your own OPENAI API KEY in streamlitDemo.py

`pip install -q streamlit langchain llama_index openai qdrant_client lxml`

`streamlit run streamlitDemo.py`

# Additional Info
Note that crawler.py needs modifying because it only output [URL,Topic Notes]

The csv file still needs Summary column

demo.csv in this folder is created manually