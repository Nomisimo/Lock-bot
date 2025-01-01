#!/bin/bash

# Define variables
SERVICE_NAME="Lock-Bot"
WORKDIR="/opt/$SERVICE_NAME"

echo "Starting the installation of $SERVICE_NAME..."

# Update and install necessary packages
echo "Updating system and installing dependencies..."
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv unzip git

# Clone the repository
echo "Cloning the repository..."
if [ -d "$WORKDIR" ]; then
    echo "Existing installation found. Removing it..."
    sudo rm -rf "$WORKDIR"
fi
sudo git clone https://github.com/Nomisimo/Lock-bot.git "$WORKDIR"

# Navigate to the working directory
cd "$WORKDIR" || exit 1

# Set up a Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create a systemd service file
echo "Creating systemd service file..."
sudo tee /etc/systemd/system/${SERVICE_NAME}.service > /dev/null <<EOF
[Unit]
Description=Nuki Lock Bot
After=network.target

[Service]
User=$USER
WorkingDirectory=$WORKDIR
ExecStart=$WORKDIR/venv/bin/python $WORKDIR/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and start the service
echo "Reloading systemd and starting the service..."
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Check the service status
echo "Checking service status..."
sudo systemctl status $SERVICE_NAME

echo "Installation completed successfully!"
