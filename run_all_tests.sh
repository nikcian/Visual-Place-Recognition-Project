#!/bin/bash
set -euo pipefail

export KMP_DUPLICATE_LIB_OK=TRUE
export PYTORCH_ENABLE_MPS_FALLBACK=1

DATASETS=(
  "tokyo_xs/test"
  "sf_xs/test"
  "svox/images/test/sun"
  "svox/images/test/night"
)

METHODS=(
  "netvlad"
  "cosplace"
  "mixvpr"
  "megaloc"
)

DISTANCES=("l2" "ip")

for ds in "${DATASETS[@]}"; do
  for method in "${METHODS[@]}"; do
    for dist in "${DISTANCES[@]}"; do
      echo "----------------------------------------------------------"
      echo "Running: $method | Dataset: $ds | Distance: $dist"
      echo "----------------------------------------------------------"

      python VPR-methods-evaluation/main.py \
        --method="$method" \
        --database_folder="data/$ds/database" \
        --queries_folder="data/$ds/queries" \
        --log_dir="outputs/$ds/${method}_${dist}" \
        --faiss_method="$dist"
    done
  done
done