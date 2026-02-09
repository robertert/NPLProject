## PJN – NLP Assignments

This repository contains selected NLP (Natural Language Processing) assignments.

- **`2/` – Project 2**: Spanish SVO sentence constructor with a dark-themed `customtkinter` GUI.  
  The app lets you build Spanish SVO sentences (subject–verb–object) with correct agreement (gender, number, tense, mood) and shows detailed logs of the morphology decisions.

- **`3/` – Project 3**: Text analysis of *Moby Dick* with dependency parsing (`spaCy`) and bipartite graphs (`networkx` + `matplotlib`).  
  It extracts adjective–noun and verb–noun collocations from the novel and visualises them as bipartite graphs, plus offers an interactive CLI for exploring collocations.

### Global requirements

- Python 3.11+ (recommended)
- Optionally [`uv`](https://github.com/astral-sh/uv) for fast virtualenv and dependency management

Each subproject (`2/`, `3/`) is self-contained and has its own:

- `README.md` – detailed description and run instructions  
- `requirements.txt` – Python dependencies for that project

### Quickstart

- **Project 2**

  ```bash
  cd 2
  python -m venv .venv
  source .venv/bin/activate  # macOS / Linux
  # .venv\Scripts\activate   # Windows
  pip install -r requirements.txt
  python main.py
  ```

- **Project 3**

  ```bash
  cd 3
  python -m venv .venv
  source .venv/bin/activate  # macOS / Linux
  # .venv\Scripts\activate   # Windows
  pip install -r requirements.txt
  python -m spacy download en_core_web_sm
  python main.py
  ```

