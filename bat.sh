#!/bin/bash

set -e

# ====================================================
# Constants / Paths
# ====================================================
VENV_DIR=".venv"
ALLURE_RESULTS="reports/allure-results"
ALLURE_HTML="reports/allure-html"
PYTEST_HTML="reports/report.html"

# ====================================================
# Step 1: Create virtual environment
# ====================================================
echo "Creating virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# ====================================================
# Step 2: Activate the virtual environment
# ====================================================
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ====================================================
# Step 3: Install required Python packages
# ====================================================
echo "Installing/updating required packages..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# ====================================================
# Step 4: Clean previous test reports
# ====================================================
echo "Cleaning previous test reports..."
rm -rf "$ALLURE_RESULTS"
rm -rf "$ALLURE_HTML"
rm -f "$PYTEST_HTML"
mkdir -p reports

# ====================================================
# Step 5: Run Pytest tests with HTML + Allure reporting
# ====================================================
echo "Running tests..."
python -m pytest -s -v \
    --reruns=2 --reruns-delay=2 \
    --alluredir="$ALLURE_RESULTS" \
    --html="$PYTEST_HTML" --self-contained-html \
    testCases/

# ====================================================
# Step 6: Generate and open Allure report
# ====================================================
if command -v allure >/dev/null 2>&1; then
    echo "Generating and opening Allure report..."
    allure generate "$ALLURE_RESULTS" -o "$ALLURE_HTML" --clean
    allure open "$ALLURE_HTML"
else
    echo "Allure CLI is not installed. Skipping Allure HTML generation."
    echo "Install it with: brew install allure"
    echo "Pytest HTML report generated at: $PYTEST_HTML"
fi
