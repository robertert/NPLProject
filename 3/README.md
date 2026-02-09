## Project 3 – Text Analysis (Moby Dick, verb–noun / adjective–noun graphs)

This directory contains the third NLP assignment:

- **`main.py`** – main analysis script
- **`moby_dick.txt`** – input corpus (Moby Dick)
- **`adj_noun_graph.png`, `verb_noun_graph.png`** – generated bipartite graphs, e.g. adjective–noun and verb–noun
- **`NPL3.pdf`** – assignment description (theory)
- **`requirements.txt`** – Python dependencies for this project

### Environment setup (.venv)

The steps below assume you have Python 3.11+ installed.

```bash
cd 3
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows (PowerShell / CMD)
python -m ensurepip --upgrade
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

Additionally, you need to download the spaCy model:

```bash
python -m spacy download en_core_web_sm
```

### Alternative – environment with `uv`

If you use [`uv`](https://github.com/astral-sh/uv), you can create the environment like this:

```bash
cd 3
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
python -m ensurepip --upgrade
pip install -U pip setuptools wheel
python -m spacy download en_core_web_sm
```

### How to run the project

After activating the environment and installing dependencies:

```bash
cd 3
python main.py
```

