#### 🇯🇵 Tokyo_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| NetVLAD (Baseline) | - | 49.8 | 62.5 | 70.5 | **78.7** |
| NetVLAD | **SuperPoint + LightGlue** | 68.3 | 72.1 | 73.7 | **78.7** |
| NetVLAD | **SuperGlue** | **69.5** | **72.7** | **74.9** | **78.7** |
| NetVLAD | **LoFTR** | 68.3 | **72.7** | 73.7 | **78.7** |

#### 🇺🇸 San Francisco_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| NetVLAD (Baseline) | - | 27.2 | 43.8 | 50.3 | **56.2** |
| NetVLAD | **SuperPoint + LightGlue** | 53.2 | **55.4** | **55.8** | **56.2** |
| NetVLAD | **SuperGlue** | 52.4 | 55.3 | **55.8** | **56.2** |
| NetVLAD | **LoFTR** | **53.6** | 55.3 | **55.8** | **56.2** |

#### 🌑 SVOX Night
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| NetVLAD (Baseline) | - | 8.0 | 17.4 | 23.1 | **29.6** |
| NetVLAD | **SuperPoint + LightGlue** | 25.4 | 27.1 | 28.4 | 29.5 |
| NetVLAD | **SuperGlue** | 13.2 | 15.2 | 16.5 | 17.8 |
| NetVLAD | **LoFTR** | **25.5** | **28.1** | **28.6** | 29.5 |

#### ☀️ SVOX Sun
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| NetVLAD (Baseline) | - | 35.4 | 52.7 | 58.8 | **65.8** |
| NetVLAD | **SuperPoint + LightGlue** | **61.7** | 63.1 | 64.2 | **65.8** |
| NetVLAD | **SuperGlue** | 46.8 | 49.7 | 50.7 | 51.4 |
| NetVLAD | **LoFTR** | 61.6 | **63.6** | **64.5** | **65.8** |



### Confronto Latenza: Global Retrieval vs Re-ranking (NetVLAD)

| Dataset | Numero Query | Latenza Global (NetVLAD) | Latenza Re-ranking (LightGlue) | Latenza Re-ranking (SuperGlue) | Latenza Re-ranking (LoFTR) | Fattore Rallentamento (NetVLAD vs LoFTR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **sf_xs** | 1000 | ~0.10s | 3.17s | 1.39s | 3.50s | **~35.0x** |
| **tokyo_xs** | 315 | ~0.10s | 3.54s | 1.39s | 3.72s | **~37.2x** |
| **svox_night** | 823 | 0.11s | 3.48s | 1.47s | 3.66s | **~33.3x** |
| **svox_sun** | 854 | 0.11s | 3.54s | 1.51s | 3.65s | **~33.2x** |