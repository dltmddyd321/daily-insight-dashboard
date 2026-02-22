#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "   Daily Insight Dashboard Automation"
echo "=========================================="

# 1. Install Dependencies (if needed)
# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is not installed."
    exit 1
fi

echo "[1/3] Checking dependencies..."
pip3 install -r "$PROJECT_ROOT/requirements.txt" -q

# 2. Run Backend to Fetch & Process Emails
echo "[2/3] Fetching emails and generating insights..."
python3 "$PROJECT_ROOT/backend/main.py"

# 3. Open Frontend
echo "[3/3] Opening Dashboard..."
open "$PROJECT_ROOT/frontend/index.html"

echo "Done! Have a productive day."
