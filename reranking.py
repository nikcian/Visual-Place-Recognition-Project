import numpy as np
from tqdm import tqdm
import os, argparse, csv
from glob import glob
from pathlib import Path
import torch

from util import get_list_distances_from_preds, read_file_preds

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--preds-dir", type=str, help="directory with predictions of a VPR model")
    parser.add_argument("--inliers-dir", type=str, help="directory with image matching results")
    parser.add_argument("--num-preds", type=int, default=100, help="number of predictions to re-rank")
    parser.add_argument(
        "--positive-dist-threshold",
        type=int,
        default=25,
        help="distance (in meters) for a prediction to be considered a positive",
    )
    parser.add_argument(
        "--recall-values",
        type=int,
        nargs="+",
        default=[1, 5, 10, 20, 100],
        help="values for recall (e.g. recall@1, recall@5)",
    )

    return parser.parse_args()

def main(args):
    preds_folder = args.preds_dir
    inliers_folder = Path(args.inliers_dir)
    num_preds = args.num_preds
    threshold = args.positive_dist_threshold
    recall_values = args.recall_values

    txt_files = glob(os.path.join(preds_folder, "*.txt"))
    txt_files.sort(key=lambda x: int(Path(x).stem))

    total_queries = len(txt_files)
    recalls = np.zeros(len(recall_values))
    
    # Lista per accumulare i dati per l'analisi statistica (Adaptive VPR / Uncertainty)
    stats_data = []

    print(f"Reranking {total_queries} queries...")
    for txt_file_query in tqdm(txt_files):
        # Carica distanze originali e risultati matching
        geo_dists_orig = torch.tensor(get_list_distances_from_preds(txt_file_query))[:num_preds]
        torch_file_query = inliers_folder.joinpath(Path(txt_file_query).name.replace('txt', 'torch'))
        
        query_results = torch.load(torch_file_query, weights_only=False)
        query_db_inliers = torch.zeros(num_preds, dtype=torch.float32)
        
        for i in range(num_preds):
            query_db_inliers[i] = query_results[i]['num_inliers']
        
        # Ordinamento in base agli inliers (Re-ranking)
        query_db_inliers_sorted, indices = torch.sort(query_db_inliers, descending=True)
        geo_dists_reranked = geo_dists_orig[indices]
        
        # --- RACCOLTA DATI PER LA RELAZIONE (Sezione 5.2 / 6.1) ---
        # Salviamo inliers del top-1 dopo il reranking e la sua correttezza
        max_inliers = query_db_inliers_sorted[0].item()
        is_correct_top1 = (geo_dists_reranked[0] <= threshold).item()
        
        stats_data.append({
            'query_id': Path(txt_file_query).stem,
            'max_inliers': max_inliers,
            'is_correct': 1 if is_correct_top1 else 0
        })

        # --- SALVATAGGIO CLASSIFICA RIORDINATA (.txt) ---
        q_path, pred_paths = read_file_preds(txt_file_query)
        pred_paths = np.array(pred_paths)[:num_preds]
        reranked_paths = pred_paths[indices.numpy()]
        
        save_txt_path = inliers_folder.joinpath(Path(txt_file_query).stem + "_reranked.txt")
        with open(save_txt_path, "w") as f:
            f.write(f"{q_path}\n")
            for p_path in reranked_paths:
                f.write(f"{p_path}\n")
        # ------------------------------------------------

        # Calcolo Recall
        for i, n in enumerate(recall_values):
            if torch.any(geo_dists_reranked[:n] <= threshold):
                recalls[i:] += 1
                break

    # --- SALVATAGGIO CSV STATISTICHE ---
    csv_path = inliers_folder.parent.joinpath(f"stats_{inliers_folder.name}.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['query_id', 'max_inliers', 'is_correct'])
        writer.writeheader()
        writer.writerows(stats_data)
    
    print(f"\n[INFO] Classifiche riordinate salvate in: {inliers_folder}")
    print(f"[INFO] Statistiche per grafici salvate in: {csv_path}")

    # Risultati finali
    recalls = recalls / total_queries * 100
    recalls_str = ", ".join([f"R@{val}: {rec:.1f}" for val, rec in zip(recall_values, recalls)])
    print(f"\nFINAL RESULTS:\n{recalls_str}")

if __name__ == "__main__":
    args = parse_arguments()
    main(args)