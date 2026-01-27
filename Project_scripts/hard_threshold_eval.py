import os
import numpy as np
import pandas as pd
import torch
import matplotlib.pyplot as plt
from glob import glob
from pathlib import Path
from tqdm import tqdm

# ==============================================================================
# CONFIG
# ==============================================================================

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

DATASET_NAME = "tokyo_xs (Test)"


TXT_PREDS_FOLDER = os.path.join(BASE_PATH, "preds")  


TORCH_FOLDER = os.path.join(BASE_PATH, "preds_superpoint-lg")  


FINAL_STATS_CSV = os.path.join(BASE_PATH, "stats_preds_superpoint-lg.csv")  

FBETA = 2.0

# ==============================================================================
# HELPERS
# ==============================================================================

def norm_qid(x) -> str | None:
    """Normalize query id to 3 digits: 7 -> '007', '7.0' -> '007'."""
    try:
        return f"{int(float(x)):03d}"
    except Exception:
        return None

def parse_preds_txt(txt_path: str) -> dict | None:
    qid = norm_qid(Path(txt_path).stem)
    if qid is None:
        return None

    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines()]

    def find_idx(prefix: str):
        for i, ln in enumerate(lines):
            if ln.lower().startswith(prefix.lower()):
                return i
        return None

    i_pred = find_idx("Predictions paths")
    i_pos = find_idx("Positives paths")

    if i_pred is None or i_pos is None or i_pos <= i_pred:
        return None

    pred_lines = [ln for ln in lines[i_pred + 1 : i_pos] if ln and not ln.endswith(":")]
    pos_lines = [ln for ln in lines[i_pos + 1 :] if ln and not ln.endswith(":")]

    if len(pred_lines) == 0:
        return None

    rank0 = pred_lines[0]
    positives = set(pos_lines)
    retrieval_is_correct = 1 if rank0 in positives else 0

    return {"query_id": qid, "retrieval_is_correct": retrieval_is_correct}

def load_retrieval_only_from_txt(txt_folder: str) -> pd.DataFrame:
    txt_files = glob(os.path.join(txt_folder, "*.txt"))
    if len(txt_files) == 0:
        raise RuntimeError(f"No .txt files found in {txt_folder}")

    txt_files.sort(key=lambda p: int(Path(p).stem))

    rows = []
    for p in tqdm(txt_files, desc="Parsing .txt retrieval"):
        d = parse_preds_txt(p)
        if d is not None:
            rows.append(d)

    if len(rows) == 0:
        raise RuntimeError("Parsed 0 txt files: check format (must contain 'Predictions paths' and 'Positives paths').")

    df = pd.DataFrame(rows)
    df["retrieval_is_correct"] = df["retrieval_is_correct"].astype(int)
    return df[["query_id", "retrieval_is_correct"]]

def load_final_stats(csv_path: str) -> pd.DataFrame:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Cannot find {csv_path}")

    df = pd.read_csv(csv_path)

    if "query_id" not in df.columns:
        raise ValueError("FINAL_STATS_CSV must contain column: query_id")

    # Compat: is_correct -> final_is_correct
    if "final_is_correct" not in df.columns:
        if "is_correct" in df.columns:
            df = df.rename(columns={"is_correct": "final_is_correct"})
        else:
            raise ValueError("FINAL_STATS_CSV must contain column: final_is_correct (or is_correct)")

    df["query_id"] = df["query_id"].apply(norm_qid)
    df = df.dropna(subset=["query_id"])
    df["final_is_correct"] = df["final_is_correct"].astype(int)

    return df[["query_id", "final_is_correct"]]

def find_torch_path(torch_folder: str, qid: str) -> str | None:
    q_int = int(qid)
    candidates = [
        os.path.join(torch_folder, f"{qid}.torch"),        # 007.torch
        os.path.join(torch_folder, f"{q_int}.torch"),      # 7.torch
        os.path.join(torch_folder, f"{q_int:05d}.torch"),  # 00007.torch
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None

def load_inliers_rank0(torch_folder: str, query_ids: list[str]) -> pd.DataFrame:
    rows = []
    missing = 0

    for qid in tqdm(query_ids, desc="Loading .torch inliers"):
        p = find_torch_path(torch_folder, qid)
        if p is None:
            missing += 1
            continue

        try:
            data = torch.load(p, weights_only=False)
            if not isinstance(data, (list, tuple)) or len(data) == 0:
                continue
            r0 = data[0]
            if "num_inliers" not in r0:
                continue
            rows.append({"query_id": qid, "inliers_rank0": int(r0["num_inliers"])})
        except Exception:
            continue

    if missing:
        print(f"⚠️ Missing .torch files: {missing}")

    if len(rows) == 0:
        raise RuntimeError("No inliers loaded from .torch. Check TORCH_FOLDER or .torch structure.")

    df = pd.DataFrame(rows)
    df["inliers_rank0"] = df["inliers_rank0"].astype(int)
    return df

# ==============================================================================
# SIMULATION
# ==============================================================================

def fbeta_like(recall01: float, saving01: float, beta: float = 2.0) -> float:
    num = (1 + beta**2) * (recall01 * saving01)
    den = (beta**2 * saving01) + recall01 + 1e-12
    return num / den

def run_simulation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Simulazione universale: il saving% rappresenta la percentuale 
    di processi di re-ranking evitati grazie alla soglia tau.
    """
    total = len(df)
    max_inl = int(df["inliers_rank0"].max())
    taus = np.unique(np.concatenate([[-1], np.arange(0, max_inl + 2)]))

    results = []
    for tau in taus:
        
        is_easy = df["inliers_rank0"].values > tau
        
        
        hits = np.where(is_easy, df["retrieval_is_correct"], df["final_is_correct"]).sum()
        recall = (hits / total) * 100.0

        
        saving = (is_easy.sum() / total) * 100.0

        r_norm, s_norm = recall / 100.0, saving / 100.0
        f2 = (1 + FBETA**2) * (r_norm * s_norm) / (FBETA**2 * s_norm + r_norm + 1e-12)

        results.append({"tau": tau, "recall@1": recall, "saving%": saving, "f2": f2})

    return pd.DataFrame(results)

def print_table(out: pd.DataFrame, step: int = 5):
    print(f"\n--- TRADE-OFF TABLE ({DATASET_NAME}) ---")
    print(f"{'Tau':<6} | {'Recall@1':<9} | {'Saving':<7} | {'F2':<8} | Note")
    print("-" * 70)

    max_rec = out["recall@1"].max()
    taus = out["tau"].values
    special = {int(taus[0]), int(taus[-1])}  

    for _, row in out.iterrows():
        tau = int(row["tau"])
        if (tau in special) or (tau >= 0 and tau % step == 0):
            note = ""
            if row["saving%"] > 40 and row["recall@1"] >= (max_rec - 1.0):
                note = "*"
            if tau == int(taus[0]):
                note = (note + " retrieval-only").strip()
            if tau == int(taus[-1]):
                note = (note + " re-rank always").strip()

            print(f"{tau:<6} | {row['recall@1']:.1f}%    | {row['saving%']:.1f}%  | {row['f2']:.4f}  | {note}")

    print("-" * 70 + "\n")

def save_plot_and_csv(out: pd.DataFrame):
    out_csv = os.path.join(BASE_PATH, f"adaptive_{DATASET_NAME.replace(' ', '_')}.csv")
    out_png = os.path.join(BASE_PATH, f"plot_{DATASET_NAME.replace(' ', '_')}_adaptive_superpoint-lg.png")

    out.to_csv(out_csv, index=False)
    print(f"✅ Saved: {out_csv}")

    plt.figure(figsize=(10, 6))
    plt.plot(out["tau"], out["recall@1"], label="Recall@1 (%)", linewidth=2)
    plt.plot(out["tau"], out["saving%"], label="Cost saving (%)", linestyle="--", linewidth=2)
    plt.xlabel("Inlier threshold (tau)")
    plt.ylabel("Percentage (%)")
    plt.title(f"Adaptive re-ranking analysis: {DATASET_NAME}")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=300)
    plt.close()
    print(f"✅ Saved: {out_png}")

# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    # 1) retrieval-only correctness dai .txt
    df_ret = load_retrieval_only_from_txt(TXT_PREDS_FOLDER)

    # 2) final correctness dal csv (dopo reranking sempre)
    df_final = load_final_stats(FINAL_STATS_CSV)

    # 3) intersection query ids (evita mismatch)
    qids = sorted(set(df_ret["query_id"].tolist()) & set(df_final["query_id"].tolist()))
    if len(qids) == 0:
        raise RuntimeError("No overlapping query_ids between TXT preds and FINAL stats CSV.")

    # 4) inliers rank0 dai .torch
    df_inl = load_inliers_rank0(TORCH_FOLDER, qids)

    # 5) merge finale
    df = (
        pd.DataFrame({"query_id": qids})
        .merge(df_ret, on="query_id", how="left")
        .merge(df_final, on="query_id", how="left")
        .merge(df_inl, on="query_id", how="left")
        .dropna()
    )

    df["retrieval_is_correct"] = df["retrieval_is_correct"].astype(int)
    df["final_is_correct"] = df["final_is_correct"].astype(int)
    df["inliers_rank0"] = df["inliers_rank0"].astype(int)

    # Baselines (sanity check)
    retrieval_only = df["retrieval_is_correct"].mean() * 100
    rerank_always = df["final_is_correct"].mean() * 100
    print(f"Retrieval-only Recall@1: {retrieval_only:.2f}%")
    print(f"Re-rank always Recall@1: {rerank_always:.2f}%")

    out = run_simulation(df)

    # Best tau by F2
    best = out.loc[out["f2"].idxmax()]
    print(
        f"Best tau by F2 (beta={FBETA}): {int(best['tau'])} | "
        f"Recall@1={best['recall@1']:.2f}% | Saving={best['saving%']:.2f}% | F2={best['f2']:.4f}"
    )

    print_table(out, step=5)
    save_plot_and_csv(out)
