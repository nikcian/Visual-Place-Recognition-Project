#!/bin/bash
set -euo pipefail

# macOS / Apple Silicon helpers
export KMP_DUPLICATE_LIB_OK=TRUE
export PYTORCH_ENABLE_MPS_FALLBACK=1

METHODS=(
  "netvlad"
  "cosplace"
  "mixvpr"
  "megaloc"
)

DISTANCES=("l2" "ip")

# --- ONLY REMAINING: SVOX ---
SVOX_DB="data/svox/images/test/gallery"

SVOX_QUERIES=()
for d in data/svox/images/test/queries_*/; do
    [ -e "$d" ] || continue
    SVOX_QUERIES+=("$(basename "$d")")
done


for qname in "${SVOX_QUERIES[@]}"; do
  QPATH="data/svox/images/test/${qname}"

  if [[ ! -d "$SVOX_DB" ]]; then
    echo "ERROR: SVOX gallery not found: $SVOX_DB"
    exit 1
  fi
  if [[ ! -d "$QPATH" ]]; then
    echo "ERROR: SVOX queries not found: $QPATH"
    exit 1
  fi

  for method in "${METHODS[@]}"; do
    for dist in "${DISTANCES[@]}"; do
      echo "----------------------------------------------------------"
      echo "Running: $method | Dataset: svox/images/test/${qname} | Distance: $dist"
      echo "DB: $SVOX_DB"
      echo "Q : $QPATH"
      echo "----------------------------------------------------------"

      python VPR-methods-evaluation/main.py \
        --method="$method" \
        --database_folder="$SVOX_DB" \
        --queries_folder="$QPATH" \
        --log_dir="outputs/svox/images/test/${qname}/${method}_${dist}" \
        --faiss_method="$dist"
    done
  done
done