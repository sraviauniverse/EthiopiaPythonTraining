#!/bin/bash

# Define the virtual environment name
VENV_NAME="myvenv"

# Update system packages
echo "Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python3 and venv module if not already installed
echo "Installing Python3 and venv module if not installed..."
sudo apt install -y python3 python3-venv

# Check if Python3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python3 is not installed. Please install Python3 before running this script."
    exit 1
fi

# Check if venv module is available
if ! python3 -m ensurepip --version &> /dev/null
then
    echo "Python3 venv module is not available. Please install it before running this script."
    exit 1
fi

# Create the virtual environment
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating virtual environment: $VENV_NAME"
    python3 -m venv $VENV_NAME
else
    echo "Virtual environment $VENV_NAME already exists."
fi

# Activate the virtual environment
source $VENV_NAME/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required Python libraries
echo "Installing required libraries: pexpect, paramiko, fabric"
pip install pexpect paramiko fabric

# Deactivate the virtual environment
echo "Deactivating virtual environment..."
deactivate

# Confirmation message
echo "Setup complete. Virtual environment $VENV_NAME is ready with the required libraries installed."
