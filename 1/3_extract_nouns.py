import stanza
import pandas as pd
from gensim.corpora import WikiCorpus
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def main():
    print("Sprawdzanie modelu Stanza dla języka fińskiego...")
    stanza.download('fi')
    
    nlp = stanza.Pipeline('fi', processors='tokenize,mwt,pos,lemma', use_gpu=False, verbose=False)

    INPUT_FILE = "fiwiki-latest-pages-articles.xml.bz2"
    wiki = WikiCorpus(INPUT_FILE, dictionary={}, processes=1)

    noun_counts = {}
    processed_sentences = 0
    TARGET_SENTENCES = 5000 

    for i, text in enumerate(wiki.get_texts()):
        if not text: continue
        
        raw_text = " ".join(text[:200])
        
        doc = nlp(raw_text)
        
        for sent in doc.sentences:
            for word in sent.words:
                if word.upos in ['NOUN', 'PROPN']:
                    lemma = word.lemma
                    if lemma:
                        noun_counts[lemma] = noun_counts.get(lemma, 0) + 1
            
            processed_sentences += 1
        
        if processed_sentences >= TARGET_SENTENCES:
            break
        
        if i % 10 == 0:
            print(f"Przetworzono artykułów: {i}, Zdań: {processed_sentences}")

    df_nouns = pd.DataFrame(list(noun_counts.items()), columns=['lemma', 'count'])
    df_nouns = df_nouns.sort_values('count', ascending=False).head(50)
    df_nouns.to_csv("fi_top_nouns.csv", index=False)

    print("\n--- TOP 10 RZECZOWNIKÓW FIŃSKICH ---")
    print(df_nouns.head(10))

if __name__ == "__main__":
    main()