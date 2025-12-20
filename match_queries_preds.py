import argparse
import numpy as np
import os
import torch
from pathlib import Path
from tqdm import tqdm
from glob import glob
import sys

# --- FIX 1: Diciamo a Python dove trovare la 'repo altra' ---
# Se la cartella esiste, la aggiungiamo al sistema
if os.path.exists("image-matching-models"):
    sys.path.append("image-matching-models")

# Gestione Importazioni
try:
    from matching import get_matcher, available_models
except ImportError:
    print("❌ ERRORE CRITICO: Non trovo il modulo 'matching'.")
    print("   Assicurati che la cartella 'image-matching-models' sia stata scaricata correttamente su Colab.")
    sys.exit(1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preds-dir", type=str, required=True)
    parser.add_argument("--out-dir", type=str, default=None)
    parser.add_argument("--matcher", type=str, default="superpoint-lg")
    parser.add_argument("--device", type=str, default="cuda")
    parser.add_argument("--im-size", type=int, default=512) # FIX 2: 512px come da progetto
    parser.add_argument("--num-preds", type=int, default=20)
    return parser.parse_args()

def main(args):
    device = args.device
    if device == "cuda" and not torch.cuda.is_available():
        print("⚠️ GPU non trovata, uso CPU.")
        device = "cpu"

    print(f"⚙️ Config: {args.matcher} | {args.im_size}px | {device}")
    
    preds_dir = Path(args.preds_dir)
    matcher = get_matcher(args.matcher, device=device)
    
    # Setup Output
    if args.out_dir:
        output_dir = Path(args.out_dir)
    else:
        output_dir = preds_dir.parent / "inliers"
    output_dir.mkdir(exist_ok=True, parents=True)

    txt_files = sorted(glob(str(preds_dir / "*.txt")))
    print(f"📂 Trovati {len(txt_files)} file.")
    
    processed = 0
    skipped = 0

    for txt_file in tqdm(txt_files):
        txt_file = Path(txt_file)
        out_file = output_dir / txt_file.with_suffix(".torch").name
        
        # --- FIX 3: RESUME (Salta se il file esiste già) ---
        if out_file.exists():
            skipped += 1
            continue
            
        with open(txt_file, "r") as f:
            lines = f.read().splitlines()
        
        if len(lines) < 4: continue
        
        # Pulizia percorsi per Colab
        q_path = lines[1].strip().replace("../", "")
        pred_paths = [l.strip().replace("../", "") for l in lines[3:3+args.num_preds] if l.strip()]
        
        results = []
        try:
            img0 = matcher.load_image(q_path, resize=args.im_size)
            for p in pred_paths:
                img1 = matcher.load_image(p, resize=args.im_size)
                res = matcher(img0, img1)
                results.append({
                    'query_path': q_path,
                    'db_path': p,
                    'num_inliers': res['num_inliers']
                })
        except:
            results = [{'num_inliers': 0} for _ in range(len(pred_paths))]
            
        torch.save(results, out_file)
        processed += 1

    print(f"✅ Finito. Processati: {processed}, Saltati: {skipped}")

if __name__ == "__main__":
    args = parse_args()
    main(args)