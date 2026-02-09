import pandas as pd
from deep_translator import GoogleTranslator

INPUT_FILE = "fi_core_stats.csv"     
OUTPUT_FILE = "fi_core_translated.csv"
LIMIT_ROWS = 30

def translate_core_stats():
    print(f"Wczytywanie pliku: {INPUT_FILE}...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"BŁĄD: Nie znaleziono pliku {INPUT_FILE}. Upewnij się, że uruchomiłeś skrypt 4!")
        return

    if 'Słowo' not in df.columns:
        print(f"BŁĄD: W pliku brakuje kolumny 'Słowo'. Dostępne kolumny: {df.columns}")
        return

    df_subset = df.head(LIMIT_ROWS).copy()
    
    print(f"Rozpoczynam tłumaczenie {len(df_subset)} słów rdzeniowych...")
    
    translator = GoogleTranslator(source='fi', target='pl')
    translations = []

    for index, row in df_subset.iterrows():
        word = row['Słowo']
        try:
            translated_word = translator.translate(word)
            
            print(f"[{index+1}/{len(df_subset)}] {word:<15} -> {translated_word}")
            translations.append(translated_word)

            
        except Exception as e:
            print(f"Błąd przy słowie '{word}': {e}")
            translations.append("ERROR")

    df_subset['Tłumaczenie_PL'] = translations

    df_subset.to_csv(OUTPUT_FILE, index=False)
    print(f"\nSUKCES! Przetłumaczona tabela rdzenia zapisana jako: {OUTPUT_FILE}")
    print("Otwórz ten plik i skopiuj dane do sekcji '4.1 Hub Words' w raporcie.")

if __name__ == "__main__":
    translate_core_stats()