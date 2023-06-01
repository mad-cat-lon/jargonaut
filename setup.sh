#!/bin/bash

OS="$(uname)"

if [[ "$OS" == "Linux" ]]; then
    echo "Detected Linux OS"
    WATCHMAN_CHECK="$(which watchman)"
    if [[ "$WATCHMAN_CHECK" == "" ]]; then
        echo "Watchman not installed. Installing now..."
        sudo apt-get update
        sudo apt-get install -y watchman
    else
        echo "Watchman is already installed"
    fi
elif [[ "$OS" == "Darwin" ]]; then
    echo "Detected macOS"
    WATCHMAN_CHECK="$(which watchman)"
    if [[ "$WATCHMAN_CHECK" == "" ]]; then
        echo "Watchman not installed. Installing now..."
        brew install watchman
    else
        echo "Watchman is already installed"
    fi
else
    echo "Unsupported operating system: $OS"
    exit 1
fi

PIP_CHECK="$(which pip)"
if [[ "$PIP_CHECK" == "" ]]; then
    echo "pip not installed. Please install pip first."
    exit 1
else
    echo "pip is already installed"
fi

echo "Installing pyre-check..."
pip install pyre-check

echo "Running 'pyre init' in the current directory..."
pyre init

echo "Starting pyre server..."
pyre start