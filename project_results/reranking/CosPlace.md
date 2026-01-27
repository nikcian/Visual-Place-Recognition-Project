#### 🇯🇵 Tokyo_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| CosPlace (Baseline) | - | 70.8 | 82.5 | 87.6 | 91.1 |
| CosPlace | **SuperPoint + LightGlue** | 86.7 | 88.3 | 88.9 | 91.1 |
| CosPlace | **SuperGlue** | 84.8 | 87.9 | 89.5 | 91.1 |
| CosPlace | **LoFTR** |  85.7 | 88.6 | 89.8 | 91.1 |

#### 🇺🇸 San Francisco_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| CosPlace (Baseline) | - | 51.8 | 67.2 | 72.5 | 77.7 |
| CosPlace | **SuperPoint + LightGlue** | 75.2 | 76.9 | 77.3 | 77.7 |
| CosPlace | **SuperGlue** | 74.2 | 76.6 | 77.2 | 77.7 |
| CosPlace | **LoFTR** | 75.0 | 76.6 | 77.1 | 77.7 |

#### 🌑 SVOX Night (Cross-Domain)
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| CosPlace (Baseline) | - | 51.6 | 68.8 | 76.1 | 80.9 |
| CosPlace | **SuperPoint + LightGlue** | 73.6 | 77.8 | 80.4 | 80.9 |
| CosPlace | **SuperGlue** | 72.4 | 77.9 | 79.3 | 80.9 |
| CosPlace | **LoFTR** | 74.4 | 78.5 | 80.3 | 80.9 |

#### ☀️ SVOX Sun
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| CosPlace (Baseline) | - | 75.9 | 88.3 | 92.2 | 94.6 |
| CosPlace | **SuperPoint + LightGlue** | 90.5 | 93.3 | 94.3 | 94.6 |
| CosPlace | **SuperGlue** | 87.4 | 93.0 | 94.0 | 94.6 |
| CosPlace | **LoFTR** | 91.3 | 93.8 | 94.0 | 94.6 |

---

### ⏱️ Analisi dell'Efficienza (Hardware: NVIDIA T4 GPU)

| Dataset | Numero Query | Latenza Global (CosPlace) | Latenza Re-ranking (SP+LG) | Latenza Re-ranking (SuperGlue) | Latenza Re-ranking (LoFTR) | Fattore Rallentamento (CosPlace vs LoFTR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **sf_xs** | 1000 | **0.08s** | 3.52s | 4.10s | **3.85s** | ~48x |
| **tokyo_xs** | 315 | **0.08s** | 3.48s | 4.05s | **3.80s** | ~47.5x |
| **svox_night** | 823 | **0.09s** | 3.56s | 4.15s | **3.90s** | ~43x |
| **svox_sun** | 854 | **0.09s** | 3.43s | 4.12s | **3.88s** | ~43x |


### 📊 Uncertainty Estimation Performance (AUPRC %) - CosPlace (ResNet50)

| Dataset | L2-Distance | PA-Score | SUE | Inliers (SP+LG) | Inliers (LoFTR) | Inliers (SuperGlue) | Random |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **tokyo_xs** | 94.3 | 91.8 | 76.9 | 99.0 | **99.2** | 99.1 | 71.5 |
| **sf_xs** | 78.2 | 77.5 | 63.6 | **98.0** | 97.3 | 96.7 | 52.4 |
| **svox_sun** | 90.2 | 89.4 | 81.2 | 97.7 | **98.5** | 97.6 | 74.9 |
| **svox_night** | 74.0 | 72.0 | 57.9 | 96.9 | **97.7** | 96.4 | 50.9 |
