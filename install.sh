#!/bin/bash

# Update apt-get
sudo apt-get update

# Check if git is installed, and if not, install it
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing Git..."
    sudo apt-get install -y git
else
    echo "Git is already installed."
fi

# Clone the repository from GitHub
git clone https://github.com/masalyuk/confessional.git

# Optionally, you can change the working directory to the cloned repository
cd confessional

# Run the prepare.sh script from the cloned repository
if [ -f "prepare.sh" ]; then
    chmod +x prepare.sh
    ./prepare.sh
else
    echo "The 'prepare.sh' script does not exist in the repository."
fi

echo "Script completed."
