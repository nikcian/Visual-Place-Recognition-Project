import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import torch
from glob import glob
from pathlib import Path
from tqdm import tqdm
from util import get_list_distances_from_preds

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preds-dir", type=str, required=True, help="Path to predictions .txt files")
    parser.add_argument("--inliers-dir", type=str, required=True, help="Path to inliers .torch files")
    parser.add_argument("--threshold", type=int, default=25, help="Positive distance threshold (meters)")
    parser.add_argument("--output-plot", type=str, default="inliers_histogram.png", help="Filename to save the plot")
    return parser.parse_args()

def main(args):
    preds_dir = Path(args.preds_dir)
    inliers_dir = Path(args.inliers_dir)
    
    txt_files = sorted(glob(str(preds_dir / "*.txt")), key=lambda x: int(Path(x).stem))
    
    correct_inliers = []
    wrong_inliers = []
    
    print("Collecting data for plots...")
    
    for txt_file in tqdm(txt_files):
        # 1. Carichiamo le distanze reali (Ground Truth)
        # util.py ci dice quanto è distante ogni predizione dalla query reale
        distances = get_list_distances_from_preds(txt_file)
        
        # 2. Carichiamo gli inliers calcolati
        torch_file = inliers_dir / Path(txt_file).name.replace('txt', 'torch')
        if not torch_file.exists(): continue
        
        res = torch.load(torch_file)
        
        # Il progetto dice: "using only the retrieval part... and the number of inliers with the first retrieved image"
        # Quindi guardiamo solo il PRIMO risultato (Top-1)
        if len(distances) > 0 and len(res) > 0:
            top1_dist = distances[0]
            top1_inliers = res[0]['num_inliers'] # Inliers del primo match
            
            # 3. Classifichiamo: Corretto o Sbagliato?
            if top1_dist <= args.threshold:
                correct_inliers.append(top1_inliers)
            else:
                wrong_inliers.append(top1_inliers)

    # --- PLOTTING ---
    plt.figure(figsize=(10, 6))
    
    # Istogramma sovrapposto
    plt.hist(correct_inliers, bins=30, alpha=0.7, label='Correct Queries (R@1)', color='green', edgecolor='black')
    plt.hist(wrong_inliers, bins=30, alpha=0.5, label='Wrong Queries', color='red', edgecolor='black')
    
    plt.title('Distribution of Inliers for Correct vs Wrong Queries')
    plt.xlabel('Number of Inliers (LightGlue)')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig(args.output_plot)
    print(f"\n📊 Plot saved to: {args.output_plot}")
    print(f"   Correct queries avg inliers: {np.mean(correct_inliers) if correct_inliers else 0:.1f}")
    print(f"   Wrong queries avg inliers:   {np.mean(wrong_inliers) if wrong_inliers else 0:.1f}")

if __name__ == "__main__":
    args = parse_args()
    main(args)