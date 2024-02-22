#!/bin/bash


# Set your OpenAI API key
export OPENAI_API_KEY="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'"

# Install required packages
pip install -r requirement.txt

# Run FastAPI application
uvicorn deploy_code:app --reload