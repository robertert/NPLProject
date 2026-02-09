# Finnish Language Corpus Analysis

A computational linguistics project that explores the statistical and semantic structure of the Finnish language using the Wikipedia corpus. The project verifies **Zipf's Law** for an agglutinative language, calculates vocabulary coverage thresholds, and identifies the "core language" using **Network Analysis** (graph theory).

## 🎯 Project Objectives
1.  **ETL & Lemmatization:** Extracting raw text from XML dumps and reducing words to their base forms (lemmas) using `Simplemma`.
2.  **Statistical Analysis:** Verifying Zipf's Law and calculating the vocabulary size required for 50-99% text comprehension.
3.  **Semantic Analysis:** Extracting top nouns and proper names using the **Stanza** neural network model (POS Tagging).
4.  **Core Language Identification:** Building a co-occurrence graph to identify "Hub Words" based on **Degree Centrality**.

## 🛠 Tech Stack
* **Language:** Python 3.12+
* **NLP & Processing:** `Gensim` (Corpus streaming), `Stanza` (Neural NLP), `Simplemma` (Lemmatization).
* **Analysis & Visualization:** `NetworkX` (Graph theory), `Pandas`, `Matplotlib`.
* **Utilities:** `Deep-translator` (Google Translate API integration).

## 📥 Data Source
* **Input:** `fiwiki-latest-pages-articles.xml.bz2`
* **Source:** [Wikimedia Dumps](https://dumps.wikimedia.org/fiwiki/latest/)

## 🚀 Usage Pipeline

Run the scripts in the following order to reproduce the analysis:

### Quickstart

```bash
cd 1
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
python 1_process_corpus.py
```