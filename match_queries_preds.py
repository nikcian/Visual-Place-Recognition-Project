import argparse
import numpy as np
import os
import torch
from pathlib import Path
from tqdm import tqdm
from glob import glob
import time
import sys

# Aggiungi il path per importare il modulo interno
sys.path.append("image-matching-models")
from matching import get_matcher, available_models

def parse_args():
    parser = argparse.ArgumentParser(description="Match queries with predictions using LightGlue/SuperGlue")
    parser.add_argument("--preds-dir", type=str, required=True, help="Path to the directory containing predictions .txt files")
    parser.add_argument("--matcher", type=str, default="superpoint-lg", choices=available_models, help="Matcher configuration")
    parser.add_argument("--device", type=str, default="cuda", help="Device to use (cuda/cpu)")
    parser.add_argument("--num-preds", type=int, default=10, help="Number of predictions to match per query")
    return parser.parse_args()

def main(args):
    device = args.device
    preds_dir = Path(args.preds_dir)
    
    # Setup output directory
    output_dir = preds_dir.parent / "inliers"
    output_dir.mkdir(exist_ok=True, parents=True)
    
    print(f"Loading matcher: {args.matcher}...")
    matcher = get_matcher(args.matcher, device=device)
    
    # Get list of prediction files
    pred_files = sorted(glob(str(preds_dir / "*.txt")))
    if len(pred_files) == 0:
        print(f"No .txt files found in {preds_dir}")
        return

    print(f"Found {len(pred_files)} query prediction files.")
    
    # Image size for resizing (optional, speeds up matching)
    img_size = 1024 

    for pred_file in tqdm(pred_files):
        pred_file = Path(pred_file)
        
        # Read the file content
        with open(pred_file, "r") as f:
            lines = f.read().splitlines()
        
        if len(lines) < 4:
            continue
            
        # FIX PERCORSI: Rimuoviamo ../ se presente per compatibilita'
        q_path = lines[1].strip()
        if q_path.startswith("../"):
            q_path = q_path.replace("../", "")
            
        cand_paths = lines[3:3+args.num_preds]
        # Pulizia percorsi candidati
        cand_paths = [p.strip().replace("../", "") if p.strip().startswith("../") else p.strip() for p in cand_paths]
        
        results = []
        
        try:
            # Load query image once
            img0 = matcher.load_image(q_path, resize=img_size)
            
            for cand_path in cand_paths:
                # Load candidate image
                img1 = matcher.load_image(cand_path, resize=img_size)
                
                # Perform matching
                pred = matcher(img0, img1)
                
                # Count inliers
                n_inliers = pred['num_inliers']
                
                results.append({
                    'query_path': q_path,
                    'db_path': cand_path,
                    'num_inliers': n_inliers
                })
                
        except Exception as e:
            # Save empty results to avoid crashing if an image is missing
            results = [{'num_inliers': 0} for _ in range(len(cand_paths))]

        # Save results for this query
        out_file = output_dir / pred_file.with_suffix(".torch").name
        torch.save(results, out_file)

    print(f"\nMatching completed. Results saved to {output_dir}")

if __name__ == "__main__":
    args = parse_args()
    main(args)