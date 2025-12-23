import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Output folder configuration
output_dir = "plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def generate_plots(csv_path, dataset_name, matcher_name):
    # Data loading
    df = pd.read_csv(csv_path)
    
    # Mapping columns: query_id, max_inliers, is_correct
    inlier_col = 'max_inliers'
    correct_col = 'is_correct'

    print(f"\n--- Generating Plots for {dataset_name} ({matcher_name}) ---")
    
    # 1. INLIERS HISTOGRAM (Exactly as in the screenshot)
    plt.figure(figsize=(10, 6))
    
    # Creating the histogram with matching labels and colors
    sns.histplot(data=df[df[correct_col] == 1], x=inlier_col, color='green', 
                 label='Correct Queries (R@1)', bins=50, alpha=0.6, element="step")
    sns.histplot(data=df[df[correct_col] == 0], x=inlier_col, color='red', 
                 label='Wrong Queries', bins=50, alpha=0.6, element="step")
    
    # Exact labels from the provided image
    plt.title('Distribution of Inliers for Correct vs Wrong Queries')
    plt.xlabel(f'Number of Inliers ({matcher_name})')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.4)
    
    plt.savefig(f"{output_dir}/{dataset_name}_{matcher_name}_distribution.png")
    plt.close()

    # 2. ADAPTIVE ANALYSIS (Recall vs Cost Saving for Section 6.1)
    max_val = int(df[inlier_col].max())
    thresholds = np.arange(0, max_val + 1, 2)
    recalls = []
    cost_savings = []
    total_queries = len(df)

    for t in thresholds:
        correct_above_t = df[(df[correct_col] == 1) & (df[inlier_col] >= t)].shape[0]
        recalls.append((correct_above_t / total_queries) * 100)
        saved_queries = df[df[inlier_col] >= t].shape[0]
        cost_savings.append((saved_queries / total_queries) * 100)

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.set_xlabel('Inlier Threshold (τ)')
    ax1.set_ylabel('Recall@1 (%)', color='tab:blue')
    ax1.plot(thresholds, recalls, marker='o', color='tab:blue', label='Recall@1', markersize=4)
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx() 
    ax2.set_ylabel('Cost Saving (%)', color='tab:green')
    ax2.plot(thresholds, cost_savings, marker='s', color='tab:green', label='Cost Saving', markersize=4)
    ax2.tick_params(axis='y', labelcolor='tab:green')

    plt.title(f'Adaptive Re-ranking Trade-off: {dataset_name} ({matcher_name})')
    fig.tight_layout()
    plt.savefig(f"{output_dir}/{dataset_name}_{matcher_name}_adaptive_tradeoff.png")
    plt.close()
    
    print(f"Plots saved to /{output_dir}")

# Update list with your actual CSV paths
files_to_process = [
    ("logs/outputs/sf_xs/mixvpr/2025-12-20_12-44-53/stats_preds_superpoint-lg.csv", "SF_XS", "LightGlue"),
    ("logs/outputs/sf_xs/mixvpr/2025-12-20_12-44-53/stats_preds_loftr.csv", "SF_XS", "LoFTR"),
    ("logs/outputs/tokyo_xs/mixvpr/2025-12-20_12-49-29/stats_preds_loftr.csv", "Tokyo", "LoFTR"),
    ("logs/outputs/svox_night/mixvpr/2025-12-20_12-55-26/stats_preds_loftr.csv", "SVOX_Night", "LoFTR"),
    ("logs/outputs/svox_sun/mixvpr/2025-12-20_12-51-56/stats_preds_loftr.csv", "SVOX_Sun", "LoFTR")
]

for path, ds, mt in files_to_process:
    if os.path.exists(path):
        generate_plots(path, ds, mt)