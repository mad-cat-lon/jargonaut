#!/bin/bash

# ANSI color codes
Reset='\033[0m'
Red='\033[0;31m'  
Green='\033[1;32m' 


# Check what OS we are running on
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
elif type lsb_release >/dev/null 2>&1; then
    OS=$(lsb_release -si)
elif [ -f /etc/lsb-release ]; then
    . /etc/lsb-release
    OS=$DISTRIB_ID
elif [ -f /etc/debian_version ]; then
    OS="Debian"
else
    OS=$(uname -s)
fi

check_for_root() {
  if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root, to install dependencies."
    echo "Please run again with root privileges or install dependencies manually."
    exit 1
  fi
}


# Install watchman
install_watchman() {
  trap "echo 'User pressed Ctrl+C \n Not exiting to avoid broken install. \n'" SIGINT 
  # Check if we are root
  check_for_root
  case $OS in
    *"Ubuntu"*)
        echo "Installing on Ubuntu"
        apt-get update -y
        apt-get install -y watchman
        ;;
    *"Debian"*)
        echo "Installing on Debian"
        apt-get update -y
        apt-get install -y watchman
        ;;
    *"CentOS"*)
        echo "Installing on CentOS must be done manually: https://facebook.github.io/watchman/docs/install.html"
        ;;
    *"Fedora"*)
       echo "Installing on Fedora must be done manually: https://facebook.github.io/watchman/docs/install.html"
        ;;
    *"Darwin"*)
        echo "Installing on Mac OS X"
        brew update
        brew install watchman
        ;;
    *)
        echo "Unsupported OS: $OS"
        echo "Please install watchman manually: https://facebook.github.io/watchman/docs/install.html"
        exit 1
        ;;
esac
}




# Check if we have watchman installed
WATCHMAN_CHECK="$(which watchman)"
if [[ "$WATCHMAN_CHECK" == "" ]]; then
  read -p "Watchman not found. Install now? [Y/n] " -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    install_watchman $OS
  else
    echo -e ".. ${Red}Please install watchman manually:${Reset} https://facebook.github.io/watchman/docs/install.html"
    exit 1
  fi 
fi

echo -e "All dependencies met! Please use a virtualenv to install python modules." 
echo -e "run ${Green}pip install -r requirements.txt${Reset} to install python dependencies"
echo -e "Then run ${Green}pyre init && pyre start${Reset} to start pyre server"

