# deepseek-rag-local
Runs deepseek locally and reads from my_codebase dir recursivelly
### Install dependencies
bash -x ./install.sh

### Create virtual env and install requirements.txt
### Prepare local codebase
Create directory my_codebase and clone git project there
Script will index files inside my_codebase and directories inside recursively

### Run the UI
streamlit run app-rag.py
Index the database if it's a first run
Ask prompt
