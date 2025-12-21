import numpy as np
import os

def read_file_preds(preds_txt_file):
    with open(preds_txt_file, "r") as file:
        lines = file.read().splitlines()
    
    if len(lines) < 2: return None, []
    
    # La query è sempre alla riga 1 (indice 1)
    query_path = lines[1].strip().replace("../", "")
    
    # Le predizioni iniziano dopo l'intestazione.
    # Nel formato NetVLAD standard spesso c'è:
    # riga 0: Query: ...
    # riga 1: path query
    # riga 2: Predictions:
    # riga 3: prima predizione
    preds_paths = []
    if len(lines) > 3:
        raw_preds = lines[3:]
        # Prende tutte le righe non vuote
        preds_paths = [p.strip().replace("../", "") for p in raw_preds if len(p.strip()) > 0]

    return query_path, preds_paths

def get_utm_from_path(path):
    # Gestione errori se il path non ha il formato atteso
    try:
        return np.array([path.split("@")[1], path.split("@")[2]]).astype(np.float32)
    except:
        return np.array([0.0, 0.0])

def compute_distance(point_A, point_B):
    return ((point_A - point_B) ** 2).sum() ** 0.5

def get_list_distances_from_preds(preds_txt_file):
    query_path, preds_paths = read_file_preds(preds_txt_file)
    if query_path is None: return []
    
    query_utm = get_utm_from_path(query_path)
    list_preds_utm = [get_utm_from_path(pred_path) for pred_path in preds_paths]
    distances = [compute_distance(query_utm, pred_utm) for pred_utm in list_preds_utm]
    return distances  # Distances are in meters