import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configurazione cartella di output
output_dir = "plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_plots(csv_path, dataset_name, matcher_name):
    # Caricamento dati
    df = pd.read_csv(csv_path)
    
    # Mapping colonne
    inlier_col = 'max_inliers'
    correct_col = 'is_correct'

    print(f"\n--- Generazione Istogramma per {dataset_name} ({matcher_name}) ---")
    
    # ISTOGRAMMA DEGLI INLIERS
    plt.figure(figsize=(10, 6))
    
    # Creazione dell'istogramma per query corrette e sbagliate
    sns.histplot(data=df[df[correct_col] == 1], x=inlier_col, color='green', 
                 label='Correct Queries (R@1)', bins=50, alpha=0.6, element="step")
    sns.histplot(data=df[df[correct_col] == 0], x=inlier_col, color='red', 
                 label='Wrong Queries', bins=50, alpha=0.6, element="step")
    
    # Etichette e stile
    plt.title(f'Distribution of Inliers: {dataset_name} ({matcher_name})')
    plt.xlabel(f'Number of Inliers')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    
    # Salvataggio
    plt.savefig(f"{output_dir}/{dataset_name}_{matcher_name}_distribution.png")
    plt.close()
    
    print(f"Grafico salvato in /{output_dir}")

# Lista dei file da processare
files_to_process = [
    ("logs/outputs/sf_xs/mixvpr/2025-12-20_12-44-53/stats_preds_superpoint-lg.csv", "SF_XS", "LightGlue"),
    ("logs/outputs/sf_xs/mixvpr/2025-12-20_12-44-53/stats_preds_loftr.csv", "SF_XS", "LoFTR"),
    ("logs/outputs/sf_xs/mixvpr/2025-12-20_12-44-53/stats_preds_superglue.csv", "SF_XS", "SuperGlue"),
    
    ("logs/outputs/tokyo_xs/mixvpr/2025-12-20_12-49-29/stats_preds_loftr.csv", "Tokyo", "LoFTR"),
    ("logs/outputs/tokyo_xs/mixvpr/2025-12-20_12-49-29/stats_preds_superglue.csv", "Tokyo", "SuperGlue"),
    ("logs/outputs/tokyo_xs/mixvpr/2025-12-20_12-49-29/stats_preds_superpoint-lg.csv", "Tokyo", "LightGlue"),
    
    ("logs/outputs/svox_night/mixvpr/2025-12-20_12-55-26/stats_preds_loftr.csv", "SVOX_Night", "LoFTR"),
    ("logs/outputs/svox_night/mixvpr/2025-12-20_12-55-26/stats_preds_superglue.csv", "SVOX_Night", "SuperGlue"),
    ("logs/outputs/svox_night/mixvpr/2025-12-20_12-55-26/stats_preds_superpoint-lg.csv", "SVOX_Night", "LightGlue"),
    
    ("logs/outputs/svox_sun/mixvpr/2025-12-20_12-51-56/stats_preds_loftr.csv", "SVOX_Sun", "LoFTR"),
    ("logs/outputs/svox_sun/mixvpr/2025-12-20_12-51-56/stats_preds_superglue.csv", "SVOX_Sun", "SuperGlue"),
    ("logs/outputs/svox_sun/mixvpr/2025-12-20_12-51-56/stats_preds_superpoint-lg.csv", "SVOX_Sun", "LightGlue"),
]

for path, ds, mt in files_to_process:
    if os.path.exists(path):
        generate_plots(path, ds, mt)
    else:
        print(f"File non trovato: {path}")