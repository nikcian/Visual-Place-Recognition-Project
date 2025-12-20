import os
import sys
import argparse
import torch
from glob import glob
from tqdm import tqdm
from pathlib import Path
from copy import deepcopy

# --- FIX 1: Importazione Semplificata per Colab ---
# Invece di percorsi complessi, puntiamo dritti alla cartella
if os.path.exists("image-matching-models"):
    sys.path.append("image-matching-models")

# Gestione errore se manca il modulo
try:
    from matching import get_matcher, available_models
    from matching.utils import get_default_device
except ImportError:
    print("❌ ERRORE: Non trovo la cartella 'image-matching-models'.")
    sys.exit(1)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--preds-dir", type=str, help="directory with predictions of a VPR model")
    parser.add_argument("--out-dir", type=str, default=None, help="output directory of image matching results")
    parser.add_argument("--matcher", type=str, default="sift-lg", choices=available_models, help="choose your matcher")
    parser.add_argument("--device", type=str, default=get_default_device(), choices=["cpu", "cuda"])
    parser.add_argument("--im-size", type=int, default=512, help="resize img to im_size x im_size")
    parser.add_argument("--num-preds", type=int, default=100, help="number of predictions to match")
    parser.add_argument("--start-query", type=int, default=-1, help="query to start from")
    parser.add_argument("--num-queries", type=int, default=-1, help="number of queries")
    return parser.parse_args()

def main(args):
    device = args.device
    
    # Fallback CPU se GPU non c'è (evita crash Colab)
    if device == "cuda" and not torch.cuda.is_available():
        print("⚠️ GPU non trovata, uso CPU.")
        device = "cpu"

    matcher_name = args.matcher
    img_size = args.im_size
    num_preds = args.num_preds
    
    print(f"⚙️ Caricamento {matcher_name} su {device}...")
    matcher = get_matcher(matcher_name, device=device)
    
    preds_folder = args.preds_dir
    start_query = args.start_query
    num_queries = args.num_queries

    output_folder = Path(preds_folder + f"_{matcher_name}") if args.out_dir is None else Path(args.out_dir)
    output_folder.mkdir(exist_ok=True, parents=True) # Parents=True evita errori se mancano cartelle intermedie
    
    txt_files = glob(os.path.join(preds_folder, "*.txt"))
    txt_files.sort(key=lambda x: int(Path(x).stem))

    start_query = start_query if start_query >= 0 else 0
    num_queries = num_queries if num_queries >= 0 else len(txt_files)

    print(f"🚀 Avvio Matching: processerò {num_queries} query (Start: {start_query})")

    # Ciclo principale
    for txt_file in tqdm(txt_files[start_query : start_query + num_queries]):
        q_num = Path(txt_file).stem
        out_file = output_folder.joinpath(f"{q_num}.torch")
        
        # --- RESUME: Se il file esiste, salta (Già presente nell'originale) ---
        if out_file.exists():
            continue
        
        results = []
        
        # --- FIX 2: Lettura file ROBUSTA (Sostituisce read_file_preds di util.py) ---
        # Questo blocco legge i file e pulisce i percorsi "../" che rompono Colab
        with open(txt_file, "r") as f:
            lines = f.read().splitlines()
        
        if len(lines) < 4: continue
            
        q_path = lines[1].strip().replace("../", "")
        # Leggiamo tutte le predizioni disponibili nel file
        all_pred_paths = lines[3:] 
        # Puliamo i percorsi delle predizioni
        pred_paths = [p.strip().replace("../", "") for p in all_pred_paths if p.strip()]
        # ---------------------------------------------------------------------------

        try:
            # Carica immagine query
            img0 = matcher.load_image(q_path, resize=img_size)
            
            # Itera sulle predizioni (fino a num_preds)
            for pred_path in pred_paths[:num_preds]:
                img1 = matcher.load_image(pred_path, resize=img_size)
                
                # Esegue il matching
                result = matcher(deepcopy(img0), img1)
                
                # Rimuove dati pesanti inutili (come nell'originale)
                result["all_desc0"] = result["all_desc1"] = None
                results.append(result)
                
        except Exception as e:
            # Se c'è un errore (es. immagine mancante), salva un risultato vuoto per non bloccare tutto
            results = [] 

        torch.save(results, out_file)

if __name__ == "__main__":
    args = parse_arguments()
    main(args)