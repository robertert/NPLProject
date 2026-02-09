import pandas as pd
from deep_translator import GoogleTranslator

INPUT_FILE = "fi_word_counts.csv"
OUTPUT_FILE = "fi_top20_translated.csv"

def process_top20():
    print(f"Wczytywanie: {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print("BŁĄD: Nie znaleziono pliku!")
        return

    top20 = df.head(20).copy()

    top20.insert(0, 'Rank', range(1, 21))
    
    translator = GoogleTranslator(source='fi', target='pl')
    translations = []
    
    print("Tłumaczenie...")
    for i, word in enumerate(top20['word']):
        try:
            trans = translator.translate(str(word))
            translations.append(trans)
            print(f"{i+1}. {word} -> {trans}")
        except Exception as e:
            print(f"Błąd przy {word}: {e}")
            translations.append("ERROR")
            
    top20['Translation'] = translations
    
    top20.to_csv(OUTPUT_FILE, index=False)
    print(f"\nGotowe! Zapisano plik: {OUTPUT_FILE}")
    print("\n--- PODGLĄD WYNIKU ---")
    print(top20.to_string(index=False))

if __name__ == "__main__":
    process_top20()