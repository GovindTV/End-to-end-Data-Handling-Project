#!/bin/bash
# init-ollama.sh

# Start Ollama server in the background
ollama serve &

# Wait for Ollama server to start
sleep 10

# Pull Llama2 1B model
ollama pull llama3.2:1b

# Keep container running
tail -f /dev/null