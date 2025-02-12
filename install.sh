#!/bin/bash
#
# This is to install the pre-requisites on the clean machine
# TODO: init venv and "pip install requirements.txt"
# TODO: create gitignore file
#
# Update and install required system packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-virtualenv

# Install Ollama
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama is already installed. Skipping..."
fi

# Download the DeepSeek-R1 model
if ! ollama list | grep -q "deepseek-r1"; then
    echo "Downloading DeepSeek-R1 model..."
    ollama pull deepseek-r1 || true
else
    echo "DeepSeek-R1 model is already downloaded. Skipping.."
fi

# Confirm installation
echo "Installation complete! Now can create venv and install the requirements.txt"