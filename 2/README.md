## Project 2 – NLP (assignment from `NLP2.pdf`)

This directory contains the second NLP assignment:

- **`main.py`** – main script with the Spanish SVO sentence constructor GUI (customtkinter)
- **`data.py`, `grammar.py`** – helper modules with lexical data and grammar logic
- **`NLP2.pdf`** – assignment description (theory)
- **`requirements.txt`** – Python dependencies for this project

### Environment setup (.venv)

The steps below assume you have Python 3.11+ installed.

```bash
cd 2
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows (PowerShell / CMD)
pip install -r requirements.txt
```

### Alternative – environment with `uv`

If you use [`uv`](https://github.com/astral-sh/uv), you can create the environment like this:

```bash
cd 2
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### How to run the project

After activating the environment and installing dependencies:

```bash
cd 2
python main.py
```

