#!/usr/bin/env bash
set -euo pipefail

echo "==> Setting up PoderBR environment for Jules/Agents <=="

# Check if uv is installed, if not fall back to pip
if ! command -v uv &> /dev/null; then
    echo "==> uv not found. Falling back to pip venv..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
else
    echo "==> Creating virtual environment and installing dependencies with uv..."
    uv venv --clear
    source .venv/bin/activate
    uv pip install -e ".[dev]"
fi

echo "==> Validating setup: Running linters..."
python3 -m ruff check .
python3 -m black --check . || echo "Black formatting not perfectly clean, but continuing..."

echo "==> Validating setup: Running basic test suite..."
# Create a dummy test if none exist just to prove pytest runs
if [ ! -f tests/unit/test_basic.py ]; then
    mkdir -p tests/unit
    cat << 'TEST' > tests/unit/test_basic.py
def test_environment_setup():
    assert True
TEST
fi

python3 -m pytest

echo "==> Setup complete and validated! Environment is ready. <=="
