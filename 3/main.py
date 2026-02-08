#!/usr/bin/env python3
"""
Analiza Semantyczna i Ekstrakcja Kolokacji - Moby Dick
Dependency parsing (spaCy) + wizualizacja grafow dwudzielnych
"""

import sys
import os
import urllib.request
from collections import Counter

import spacy
import networkx as nx
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from colorama import init, Fore, Style

init(autoreset=True)

GUTENBERG_URL = "https://www.gutenberg.org/files/2701/2701-0.txt"
CACHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "moby_dick.txt")


def download_text(url=GUTENBERG_URL, cache_path=CACHE_PATH):
    """Pobiera tekst z Project Gutenberg, cachuje lokalnie."""
    if os.path.exists(cache_path):
        print(f"Wczytywanie z cache: {cache_path}")
        with open(cache_path, "r", encoding="utf-8") as f:
            return f.read()
    print(f"Pobieranie tekstu z {url} ...")
    with urllib.request.urlopen(url) as resp:
        raw = resp.read().decode("utf-8")
    with open(cache_path, "w", encoding="utf-8") as f:
        f.write(raw)
    print(f"Zapisano do {cache_path} ({len(raw)} znakow)")
    return raw


def clean_text(raw_text):
    """Usuwa naglowki/stopki Gutenberg, normalizuje whitespace."""
    start_marker = "*** START OF THE PROJECT GUTENBERG EBOOK"
    end_marker = "*** END OF THE PROJECT GUTENBERG EBOOK"

    start_idx = raw_text.find(start_marker)
    if start_idx != -1:
        start_idx = raw_text.index("\n", start_idx) + 1
    else:
        start_idx = 0

    end_idx = raw_text.find(end_marker)
    if end_idx == -1:
        end_idx = len(raw_text)

    text = raw_text[start_idx:end_idx].strip()

    # Normalizacja whitespace (zachowujemy paragrafy)
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        cleaned_lines.append(" ".join(line.split()))
    text = "\n".join(cleaned_lines)

    word_count = len(text.split())
    print(f"Tekst oczyszczony: {word_count} slow")
    return text


def process_text(text, nlp):
    """Przetwarza tekst przez spaCy, ekstrahuje kolokacje adj+noun i verb+noun."""
    adj_noun = Counter()
    verb_noun = Counter()

    # Dzielenie na paragrafy
    chunks = [p.strip() for p in text.split("\n\n") if p.strip()]
    print(f"Liczba chunkow: {len(chunks)}")

    for i, doc in enumerate(nlp.pipe(chunks, batch_size=50)):
        if (i + 1) % 200 == 0:
            print(f"  Przetworzono {i + 1}/{len(chunks)} chunkow...")

        for token in doc:
            # amod: przymiotnik -> rzeczownik (head)
            if token.dep_ == "amod" and token.head.pos_ == "NOUN":
                adj = token.lemma_.lower()
                noun = token.head.lemma_.lower()
                if adj.isalpha() and noun.isalpha():
                    adj_noun[(adj, noun)] += 1

            # dobj: rzeczownik (dopelnienie) -> czasownik (head)
            if token.dep_ == "dobj" and token.pos_ == "NOUN":
                noun = token.lemma_.lower()
                verb = token.head.lemma_.lower()
                if noun.isalpha() and verb.isalpha():
                    verb_noun[(verb, noun)] += 1

            # nsubj: rzeczownik (podmiot) -> czasownik (head)
            if token.dep_ == "nsubj" and token.pos_ == "NOUN":
                noun = token.lemma_.lower()
                verb = token.head.lemma_.lower()
                if noun.isalpha() and verb.isalpha():
                    verb_noun[(verb, noun)] += 1

    print(f"Znaleziono {len(adj_noun)} unikalnych par przymiotnik+rzeczownik")
    print(f"Znaleziono {len(verb_noun)} unikalnych par czasownik+rzeczownik")
    return adj_noun, verb_noun


def build_keyword_index(pair_counter):
    """Buduje indeks {keyword: [(noun, count), ...]} posortowany po lacznej czestosci."""
    index = {}
    for (keyword, noun), count in pair_counter.items():
        if keyword not in index:
            index[keyword] = []
        index[keyword].append((noun, count))

    # Sortuj partnow wewnatrz kazdego keyword
    for keyword in index:
        index[keyword].sort(key=lambda x: x[1], reverse=True)

    # Sortuj keywords po lacznej czestosci
    sorted_index = dict(
        sorted(index.items(), key=lambda x: sum(c for _, c in x[1]), reverse=True)
    )
    return sorted_index


def print_rankings(keyword_index, relation_name, top_n=30):
    """Wyswietla ranking slow kluczowych z ich partnerami."""
    print(f"\n{'='*60}")
    print(f"  TOP {top_n} - {relation_name}")
    print(f"{'='*60}")

    for rank, (keyword, partners) in enumerate(list(keyword_index.items())[:top_n], 1):
        total = sum(c for _, c in partners)
        top_partners = partners[:10]
        partners_str = ", ".join(f"{n}[{c}]" for n, c in top_partners)
        print(f"{rank:>3}. {keyword} (total: {total}): {partners_str}")


def draw_bipartite_graph(pair_counter, title, filename, top_n=100):
    """Rysuje graf dwudzielny i zapisuje do PNG."""
    # Top keywords wg czestosci
    keyword_freq = Counter()
    for (kw, _), count in pair_counter.items():
        keyword_freq[kw] += count
    top_keywords = {kw for kw, _ in keyword_freq.most_common(top_n)}

    # Filtruj krawedzie: tylko top keywords, waga >= 2
    edges = []
    for (kw, noun), count in pair_counter.items():
        if kw in top_keywords and count >= 2:
            edges.append((kw, noun, count))

    if not edges:
        print(f"Brak krawedzi do narysowania dla {title}")
        return

    G = nx.Graph()
    keywords_set = set()
    nouns_set = set()
    max_weight = max(w for _, _, w in edges)

    for kw, noun, weight in edges:
        kw_node = f"K:{kw}"
        noun_node = f"N:{noun}"
        G.add_node(kw_node, bipartite=0)
        G.add_node(noun_node, bipartite=1)
        G.add_edge(kw_node, noun_node, weight=weight)
        keywords_set.add(kw_node)
        nouns_set.add(noun_node)

    # Layout
    pos = {}
    kw_list = sorted(keywords_set)
    noun_list = sorted(nouns_set)
    for i, node in enumerate(kw_list):
        pos[node] = (0, i)
    for i, node in enumerate(noun_list):
        pos[node] = (1, i * (len(kw_list) / max(len(noun_list), 1)))

    fig, ax = plt.subplots(figsize=(40, 30), dpi=150)
    ax.set_title(title, fontsize=16, fontweight="bold")

    # Rysuj krawedzie z przezroczystoscia
    for u, v, data in G.edges(data=True):
        w = data["weight"]
        alpha = min(0.2 + 0.8 * (w / max_weight), 1.0)
        width = 0.3 + 2.0 * (w / max_weight)
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            color="gray",
            alpha=alpha,
            linewidth=width,
        )

    # Rysuj wezly
    for node in kw_list:
        ax.plot(pos[node][0], pos[node][1], "o", color="green", markersize=6)
        ax.text(
            pos[node][0] - 0.02,
            pos[node][1],
            node[2:],
            fontsize=5,
            ha="right",
            va="center",
            color="green",
        )
    for node in noun_list:
        ax.plot(pos[node][0], pos[node][1], "o", color="blue", markersize=4)
        ax.text(
            pos[node][0] + 0.02,
            pos[node][1],
            node[2:],
            fontsize=5,
            ha="left",
            va="center",
            color="blue",
        )

    ax.set_xlim(-0.3, 1.3)
    ax.axis("off")
    plt.tight_layout()

    filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    plt.savefig(filepath, bbox_inches="tight")
    plt.close()
    print(f"Graf zapisany: {filepath}")


def interactive_cli(adj_noun, verb_noun):
    """Interaktywne CLI do przeszukiwania kolokacji."""
    print(f"\n{'='*60}")
    print("  INTERAKTYWNE CLI - Wyszukiwanie kolokacji")
    print(f"{'='*60}")
    print("Wpisz 1 slowo (szuka partnerow) lub 2 slowa (sprawdza pare)")
    print("Wyjscie: quit / exit / q\n")

    def color_count(count):
        if count == 0:
            return Fore.RED + str(count) + Style.RESET_ALL
        elif count == 1:
            return Fore.YELLOW + str(count) + Style.RESET_ALL
        elif count <= 10:
            return Fore.GREEN + str(count) + Style.RESET_ALL
        else:
            return Fore.BLUE + str(count) + Style.RESET_ALL

    def color_label(count):
        if count == 0:
            return Fore.RED + "nie wystepuje" + Style.RESET_ALL
        elif count == 1:
            return Fore.YELLOW + "rzadkie" + Style.RESET_ALL
        elif count <= 10:
            return Fore.GREEN + "umiarkowane" + Style.RESET_ALL
        else:
            return Fore.BLUE + "czeste" + Style.RESET_ALL

    while True:
        try:
            query = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nDo widzenia!")
            break

        if query.lower() in ("quit", "exit", "q"):
            print("Do widzenia!")
            break

        if not query:
            continue

        words = query.lower().split()

        if len(words) == 2:
            w1, w2 = words
            # Sprawdz pare w obu kierunkach i obu Counterach
            adj_count = adj_noun.get((w1, w2), 0) + adj_noun.get((w2, w1), 0)
            verb_count = verb_noun.get((w1, w2), 0) + verb_noun.get((w2, w1), 0)
            total = adj_count + verb_count

            print(f"  Para: '{w1}' + '{w2}'")
            print(f"    adj+noun:  {color_count(adj_count)}  {color_label(adj_count)}")
            print(f"    verb+noun: {color_count(verb_count)}  {color_label(verb_count)}")
            print(f"    lacznie:   {color_count(total)}  {color_label(total)}")

        elif len(words) == 1:
            word = words[0]
            print(f"  Szukam kolokacji dla: '{word}'\n")

            # Jako keyword w adj_noun
            adj_partners = Counter()
            for (kw, noun), count in adj_noun.items():
                if kw == word:
                    adj_partners[noun] += count
            if adj_partners:
                print(f"  Jako przymiotnik (adj+noun) - top 15:")
                for noun, c in adj_partners.most_common(15):
                    print(f"    {noun}: {color_count(c)}")

            # Jako noun w adj_noun
            adj_kw_partners = Counter()
            for (kw, noun), count in adj_noun.items():
                if noun == word:
                    adj_kw_partners[kw] += count
            if adj_kw_partners:
                print(f"  Jako rzeczownik (adj+noun) - top 15 przymiotnikow:")
                for kw, c in adj_kw_partners.most_common(15):
                    print(f"    {kw}: {color_count(c)}")

            # Jako keyword w verb_noun
            verb_partners = Counter()
            for (kw, noun), count in verb_noun.items():
                if kw == word:
                    verb_partners[noun] += count
            if verb_partners:
                print(f"  Jako czasownik (verb+noun) - top 15:")
                for noun, c in verb_partners.most_common(15):
                    print(f"    {noun}: {color_count(c)}")

            # Jako noun w verb_noun
            verb_kw_partners = Counter()
            for (kw, noun), count in verb_noun.items():
                if noun == word:
                    verb_kw_partners[kw] += count
            if verb_kw_partners:
                print(f"  Jako rzeczownik (verb+noun) - top 15 czasownikow:")
                for kw, c in verb_kw_partners.most_common(15):
                    print(f"    {kw}: {color_count(c)}")

            if not (adj_partners or adj_kw_partners or verb_partners or verb_kw_partners):
                print(f"  {Fore.RED}Nie znaleziono kolokacji dla '{word}'{Style.RESET_ALL}")
        else:
            print("  Wpisz 1 lub 2 slowa.")


def main():
    print("=" * 60)
    print("  Analiza Semantyczna - Ekstrakcja Kolokacji")
    print("  Korpus: Moby Dick (Herman Melville)")
    print("=" * 60)

    # 1. Pobieranie tekstu
    raw_text = download_text()

    # 2. Czyszczenie
    text = clean_text(raw_text)

    # 3. Ladowanie modelu spaCy
    print("Ladowanie modelu spaCy (en_core_web_sm)...")
    nlp = spacy.load("en_core_web_sm")
    nlp.max_length = 1_500_000
    print("Model zaladowany.")

    # 4. Przetwarzanie
    print("\nRozpoczynanie analizy dependency parsing...")
    adj_noun, verb_noun = process_text(text, nlp)

    # 5. Rankingi
    adj_index = build_keyword_index(adj_noun)
    verb_index = build_keyword_index(verb_noun)
    print_rankings(adj_index, "Przymiotnik + Rzeczownik (amod)", top_n=30)
    print_rankings(verb_index, "Czasownik + Rzeczownik (dobj/nsubj)", top_n=30)

    # 6. Grafy
    print("\nGenerowanie grafow...")
    draw_bipartite_graph(adj_noun, "Kolokacje: Przymiotnik + Rzeczownik (Moby Dick)", "adj_noun_graph.png")
    draw_bipartite_graph(verb_noun, "Kolokacje: Czasownik + Rzeczownik (Moby Dick)", "verb_noun_graph.png")

    # 7. Interaktywne CLI
    interactive_cli(adj_noun, verb_noun)


if __name__ == "__main__":
    main()
