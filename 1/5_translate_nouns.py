import pandas as pd
from deep_translator import GoogleTranslator

INPUT_FILE = "fi_top_nouns.csv" 
OUTPUT_FILE = "fi_nouns_translated.csv"
LIMIT_ROWS = 50 

def translate_csv():
    print(f"wczytywanie pliku: {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {INPUT_FILE}. Sprawdź nazwę!")
        return

    if 'lemma' in df.columns:
        col_name = 'lemma'
    elif 'word' in df.columns:
        col_name = 'word'
    else:
        print("BŁĄD: Nie znaleziono kolumny 'lemma' ani 'word' w pliku CSV.")
        print(f"Dostępne kolumny: {df.columns}")
        return

    df_subset = df.head(LIMIT_ROWS).copy()
    
    print(f"Rozpoczynam tłumaczenie {len(df_subset)} słów z fińskiego na polski...")
    print("To może chwilę potrwać (dodajemy opóźnienia, aby nie zablokować API).")

    translator = GoogleTranslator(source='fi', target='pl')
    translations = []

    for index, row in df_subset.iterrows():
        word = row[col_name]
        try:
            translated_word = translator.translate(word)
            translations.append(translated_word)
            
            print(f"[{index+1}/{len(df_subset)}] {word} -> {translated_word}")
            
            
        except Exception as e:
            print(f"Błąd przy słowie '{word}': {e}")
            translations.append("ERROR")

    df_subset['polish_translation'] = translations

    df_subset.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSUKCES! Przetłumaczony plik zapisano jako: {OUTPUT_FILE}")
    print("Możesz teraz skopiować te dane do tabeli w raporcie.")

if __name__ == "__main__":
    translate_csv()