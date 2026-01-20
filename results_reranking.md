### 📊 Risultati Comparativi: Recall@N

#### 🇯🇵 Tokyo_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 78.1 | 89.5 | 92.4 | 93.7 |
| MixVPR | **SuperGlue** | 87.0 | 91.7 | 93.0 | 93.7 |
| MixVPR | **SuperPoint + LightGlue** | 88.9 | **92.4** | 93.0 | **93.7** |
| MixVPR | **LoFTR** | **89.8** | **92.4** | **93.7** | **93.7** |

#### 🇺🇸 San Francisco_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 70.2 | 79.0 | 81.3 | 83.9 |
| MixVPR | **SuperPoint + LightGlue** | **81.0** | **83.3** | **83.7** | **83.9** |
| MixVPR | **SuperGlue** | 80.3 | 82.7 | 83.5 | 83.9 |
| MixVPR | **LoFTR** | 80.1 | 82.9 | 83.6 | **83.9** |

#### 🌑 SVOX Night (Cross-Domain)
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 62.9 | 79.8 | 84.1 | 88.0 |
| MixVPR | **SuperPoint + LightGlue** | 82.0 | 86.4 | 87.1 | **88.0** |
| MixVPR | **SuperGlue** | 82.0 | 86.6 | 87.4 | **88.0** |
| MixVPR | **LoFTR** | **82.5** | **86.8** | **87.6** | **88.0** |

#### ☀️ SVOX Sun
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 85.4 | 93.0 | 94.7 | 95.9 |
| MixVPR | **SuperPoint + LightGlue** | 91.5 | **95.2** | **95.7** | **95.9** |
| MixVPR | **SuperGlue** | 89.9 | 94.3 | 95.6 | 95.9 |
| MixVPR | **LoFTR** | **93.6** | 94.8 | 95.6 | **95.9** |

---

## ⏱️ Analisi dell'Efficienza (Hardware: Apple M4 Pro)



| Dataset | Numero Query | Latenza Global (MixVPR) | Latenza Re-ranking (SP+LG) | Latenza Re-ranking (SuperGlue) | Latenza Re-ranking (LoFTR) | Fattore Rallentamento (MixVPR vs LoFTR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **sf_xs** | 1000 | **0.21s** | 4.63s | 3.64s | **3.27s** | ~15.5x |
| **tokyo_xs** | 315 | **0.39s** | 4.58s | 8.04s | **3.34s** | ~8.5x |
| **svox_night** | 823 | **0.19s** | 4.56s | 17.18s | **3.22s** | ~17x |
| **svox_sun** | 854 | **0.19s** | 4.53s | 8.19s (CPU) | **3.27s** | ~17.2x |


