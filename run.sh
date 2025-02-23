#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Set environment variables for better resource management
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=5
export STREAMLIT_BROWSER_FILE_WATCHER_TYPE=none
export PYTHONUNBUFFERED=1

# Run the Streamlit app with proper resource allocation
streamlit run app.py --server.maxUploadSize=5 --server.maxMessageSize=100
