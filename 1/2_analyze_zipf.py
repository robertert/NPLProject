import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("fi_word_counts.csv")

df['rank'] = df.index + 1

plt.figure(figsize=(10, 6))
plt.loglog(df['rank'], df['count'], marker='.', linestyle='none', markersize=2, alpha=0.5)
plt.title('Prawo Zipfa - Korpus Fiński')
plt.xlabel('Ranga (skala log)')
plt.ylabel('Częstotliwość (skala log)')
plt.grid(True, which="both", ls="-", alpha=0.2)
plt.savefig('zipf_finnish.png')
print("Wykres Zipfa zapisano jako 'zipf_finnish.png'")

total_tokens = df['count'].sum()
df['cumulative_percent'] = df['count'].cumsum() / total_tokens

thresholds = [0.5, 0.8, 0.9, 0.95, 0.99]

print("\n--- POKRYCIE TEKSTU ---")
print(f"Całkowita liczba tokenów: {total_tokens}")
print(f"Całkowita liczba unikalnych słów: {len(df)}")

coverage_data = []

for t in thresholds:
    try:
        count_needed = df[df['cumulative_percent'] >= t].index[0] + 1
    except IndexError:
        count_needed = len(df)
        
    percent_vocab = (count_needed / len(df)) * 100
    
    print(f"Aby zrozumieć {t*100}% tekstu, trzeba znać {count_needed} słów ({percent_vocab:.2f}% słownictwa).")
    
    coverage_data.append({
        "Pokrycie_tekstu": f"{t*100:.0f}%",
        "Wymagana_liczba_slow": count_needed,
        "Procent_slownictwa": round(percent_vocab, 4)
    })

output_csv = "fi_coverage_stats.csv"
df_coverage = pd.DataFrame(coverage_data)
df_coverage.to_csv(output_csv, index=False)

print(f"\nZapisano tabelę pokrycia do pliku: {output_csv}")