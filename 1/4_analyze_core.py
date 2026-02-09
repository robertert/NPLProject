import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from gensim.corpora import WikiCorpus
import itertools
import logging
import math

INPUT_CORPUS = "fiwiki-latest-pages-articles.xml.bz2"
INPUT_COUNTS = "fi_word_counts.csv"
OUTPUT_STATS_CSV = "fi_core_stats.csv"
TOP_N_WORDS = 30
LIMIT_ARTICLES = 10000

FINNISH_STOPWORDS = {
    "olla", "ei", "ja", "se", "hän", "joka", "että", "tämä", "kuin", 
    "mutta", "ne", "kun", "myös", "voida", "niin", "tai", "saada", 
    "vain", "mukaan", "jos", "tulla", "jokin", "vuosi", "koko"
}

def analyze_core():
    print("1. Wczytywanie statystyk słów...")
    try:
        df = pd.read_csv(INPUT_COUNTS)
    except FileNotFoundError:
        print("BŁĄD: Nie znaleziono pliku fi_word_counts.csv. Uruchom najpierw skrypt 1!")
        return

    mask = (~df['word'].isin(FINNISH_STOPWORDS)) & (df['word'].str.len() > 2)
    top_words_df = df[mask].head(TOP_N_WORDS)
    
    top_words_set = set(top_words_df['word'].values)
    print(f"Wybrane słowa do rdzenia: {top_words_set}")

    G = nx.Graph()
    G.add_nodes_from(top_words_set)

    print(f"2. Skanowanie korpusu w poszukiwaniu powiązań (limit: {LIMIT_ARTICLES} art)...")
    wiki = WikiCorpus(INPUT_CORPUS, dictionary={}, processes=1)
    
    pair_counts = {}

    for i, text in enumerate(wiki.get_texts()):
        if i >= LIMIT_ARTICLES:
            break
            
        filtered_tokens = [token for token in text if token in top_words_set]
        
        for w1, w2 in zip(filtered_tokens, filtered_tokens[1:]):
            if w1 == w2: continue 
            pair = tuple(sorted((w1, w2)))
            pair_counts[pair] = pair_counts.get(pair, 0) + 1

    print("3. Budowanie grafu...")
    MIN_COOCCURRENCE = 5
    for (w1, w2), count in pair_counts.items():
        if count >= MIN_COOCCURRENCE:
            G.add_edge(w1, w2, weight=count)

    print("3a. Obliczanie miar centralności i zapis do pliku...")
    
    degree_dict = dict(G.degree())
    
    norm_centrality = nx.degree_centrality(G)
    
    stats_data = []
    for word in G.nodes():
        deg = degree_dict.get(word, 0)
        norm = norm_centrality.get(word, 0.0)
        
        stats_data.append({
            "Słowo": word,
            "Liczba_sasiadow": deg,
            "Centralnosc_norm": round(norm, 4)
        })
    
    df_stats = pd.DataFrame(stats_data)
    
    df_stats = df_stats.sort_values(by="Liczba_sasiadow", ascending=False)
    
    df_stats.insert(0, 'Ranga', range(1, len(df_stats) + 1))
    
    df_stats.to_csv(OUTPUT_STATS_CSV, index=False)
    print(f"--> Zapisano szczegółowe statystyki do: {OUTPUT_STATS_CSV}")
    
    print("\n--- HUB WORDS (Top 15) ---")
    print(df_stats.head(15).to_string(index=False))
    print("\nGenerowanie wykresu...")
    plt.figure(figsize=(20, 20))
    
    if G.number_of_nodes() > 0:
        optimal_k = 3.0 / math.sqrt(G.number_of_nodes())
    else:
        optimal_k = 0.5

    pos = nx.spring_layout(G, k=0.8, iterations=100, seed=42)
    
    weights = [G[u][v]['weight'] for u, v in G.edges()]
    if weights:
        width = [math.log(w) * 0.5 for w in weights]
    else:
        width = 1.0
    
    nx.draw_networkx_edges(G, pos, width=width, alpha=0.2, edge_color="gray")
    
    node_sizes = [degree_dict.get(n, 1) * 150 for n in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color="#69b3a2", alpha=0.9)
    
    nx.draw_networkx_labels(G, pos, font_size=12, font_family="sans-serif", font_weight="bold",
                            bbox=dict(facecolor='white', edgecolor='none', alpha=0.7, pad=0.5))

    plt.title(f"Rdzeń Języka Fińskiego (Top {TOP_N_WORDS} words co-occurrence)", fontsize=20)
    plt.axis('off')
    
    plt.savefig("fi_core_graph.png", dpi=300, bbox_inches='tight')
    print("Zapisano czytelniejszy graf jako 'fi_core_graph.png'")

if __name__ == "__main__":
    analyze_core()