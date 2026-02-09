import logging
from gensim.corpora import WikiCorpus
from simplemma import lemmatize
from collections import Counter
import pandas as pd
import time

INPUT_FILE = "fiwiki-latest-pages-articles.xml.bz2" 
OUTPUT_FILE = "fi_word_counts.csv"
LANG_CODE = "fi"

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def process_wiki_dump():
    print(f"Rozpoczynam przetwarzanie: {INPUT_FILE}")
    
    wiki = WikiCorpus(INPUT_FILE, dictionary={})
    
    word_counts = Counter()
    total_tokens = 0
    
    start_time = time.time()
    
    for i, text in enumerate(wiki.get_texts()):
        lemmatized_tokens = []
        for token in text:
            lemma = lemmatize(token, lang=LANG_CODE)
            lemmatized_tokens.append(lemma)
            
        word_counts.update(lemmatized_tokens)
        total_tokens += len(lemmatized_tokens)
        
        if i % 1000 == 0:
            elapsed = time.time() - start_time
            print(f"Przetworzono {i} artykułów. Tokenów: {total_tokens}. Czas: {elapsed:.0f}s")
            
    print(f"Zakończono. Łącznie tokenów: {total_tokens}")
    print(f"Unikalnych słów (types): {len(word_counts)}")
    
    df = pd.DataFrame(word_counts.most_common(), columns=['word', 'count'])
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Zapisano wyniki do {OUTPUT_FILE}")

if __name__ == "__main__":
    process_wiki_dump()