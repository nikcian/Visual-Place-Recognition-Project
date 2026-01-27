### 📊 Risultati Comparativi: Recall@N

#### 🇯🇵 Tokyo_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MegaLoc (Baseline) | - | **95.6** | 97.8 | **98.7** | **99.0** |
| MegaLoc | **SuperPoint + LightGlue** | 94.3 | **98.4** | **98.7** | **99.0** |
| MegaLoc | **SuperGlue** | 93.0 | 98.1 | 98.4 | **99.0** |
| MegaLoc | **LoFTR** | 94.3 | 97.8 | **98.7** | **99.0** |

#### 🇺🇸 San Francisco_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MegaLoc (Baseline) | - | 86.9 | 90.4 | 91.2 | **91.5** |
| MegaLoc | **SuperPoint + LightGlue** | **87.0** | **90.6** | **91.3** | **91.5** |
| MegaLoc | **SuperGlue** | 85.8 | 89.9 | 90.7 | **91.5** |
| MegaLoc | **LoFTR** | 86.5 | 89.7 | 90.8 | **91.5** |

#### 🌑 SVOX Night
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MegaLoc (Baseline) | - | **96.5** | **98.7** | **99.0** | **99.3** |
| MegaLoc | **SuperPoint + LightGlue** | 91.1 | 97.4 | 98.9 | **99.3** |
| MegaLoc | **SuperGlue** | 90.5 | 97.6 | 98.7 | **99.3** |
| MegaLoc | **LoFTR** | 92.6 | 98.4 | **99.0** | **99.3** |

#### ☀️ SVOX Sun
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MegaLoc (Baseline) | - | 97.2 | **99.3** | **99.5** | **99.6** |
| MegaLoc | **SuperPoint + LightGlue** | 96.0 | 99.1 | 99.4 | **99.6** |
| MegaLoc | **SuperGlue** | 93.8 | 98.7 | 99.4 | **99.6** |
| MegaLoc | **LoFTR** | **97.3** | **99.3** | **99.5** | **99.6** |

---

## ⏱️ Analisi dell'Efficienza (Hardware: NVIDIA T4 GPU on Colab)



| Dataset | Numero Query | Latenza Global (MegaLoc) | Latenza Re-ranking (SP+LG) | Latenza Re-ranking (SuperGlue) | Latenza Re-ranking (LoFTR) | Fattore Rallentamento (MegaLoc vs LoFTR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **sf_xs** | 1000 | 0.10s | 3.51s | 1.46s | 3.50s | ~35x |
| **tokyo_xs** | 315 | 0.10s | 3.49s | 1.48s | 3.49s | ~34.9x |
| **svox_night** | 823 | 0.10s | 3.53s | 1.50s | 3.48s | ~34.8x |
| **svox_sun** | 854 | 0.10s | 3.45s | 1.52s | 3.42s | ~34.2x |


