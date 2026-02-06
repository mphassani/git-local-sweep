#!/bin/bash
set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Installing git-local-sweep..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    echo "Please install Python 3 and try again."
    exit 1
fi

# Determine installation directory
if [ -w "/usr/local/bin" ]; then
    INSTALL_DIR="/usr/local/bin"
elif [ -d "$HOME/.local/bin" ] && [[ ":$PATH:" == *":$HOME/.local/bin:"* ]]; then
    INSTALL_DIR="$HOME/.local/bin"
else
    INSTALL_DIR="$HOME/.local/bin"
    mkdir -p "$INSTALL_DIR"
    echo -e "${YELLOW}Note: Installing to $INSTALL_DIR${NC}"

    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        echo -e "${YELLOW}Warning: $INSTALL_DIR is not in your PATH.${NC}"
        echo "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo -e "${GREEN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
        echo ""
    fi
fi

# Download the script
SCRIPT_URL="https://raw.githubusercontent.com/phassani/git-local-sweep/main/git-local-sweep"
TEMP_FILE=$(mktemp)

echo "Downloading git-local-sweep..."
if command -v curl &> /dev/null; then
    curl -fsSL "$SCRIPT_URL" -o "$TEMP_FILE"
elif command -v wget &> /dev/null; then
    wget -qO "$TEMP_FILE" "$SCRIPT_URL"
else
    echo -e "${RED}Error: Neither curl nor wget is installed.${NC}"
    echo "Please install curl or wget and try again."
    rm "$TEMP_FILE"
    exit 1
fi

# Make it executable
chmod +x "$TEMP_FILE"

# Move to installation directory
if [ -w "$INSTALL_DIR" ]; then
    mv "$TEMP_FILE" "$INSTALL_DIR/git-local-sweep"
    ln -sf "$INSTALL_DIR/git-local-sweep" "$INSTALL_DIR/gls"
else
    echo "Installing to $INSTALL_DIR requires sudo privileges."
    sudo mv "$TEMP_FILE" "$INSTALL_DIR/git-local-sweep"
    sudo ln -sf "$INSTALL_DIR/git-local-sweep" "$INSTALL_DIR/gls"
fi

echo -e "${GREEN}✓ Successfully installed git-local-sweep to $INSTALL_DIR${NC}"
echo -e "${GREEN}✓ Alias installed: gls${NC}"
echo ""
echo "Usage:"
echo "  git-local-sweep preview  - Preview branches to be deleted"
echo "  git-local-sweep cleanup  - Delete branches (with confirmation)"
echo "  gls preview              - Same as git-local-sweep preview"
echo "  gls cleanup              - Same as git-local-sweep cleanup"
echo ""
echo "Try it now: cd into a git repository and run 'git-local-sweep preview'"
