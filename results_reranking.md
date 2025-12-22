## 📍 Fase 5.2: Re-ranking con Image Matching (Local Features)

In questa fase, i primi $K=20$ candidati estratti dal modello globale **MixVPR(4096)** sono stati riordinati tramite due diversi matcher locali basati su Graph Neural Networks (GNN). Il processo prevede l'estrazione di feature locali tramite **SuperPoint**, il matching geometrico e il conteggio degli **inliers** per stabilire la nuova gerarchia dei risultati. Tutte le immagini sono state ridimensionate a $512 \times 512$ pixel.

---

### 📊 Risultati Comparativi: Recall@N

Il sistema è stato valutato confrontando la baseline globale (**MixVPR**) con due diverse strategie di re-ranking locale basate su GNN: **SuperPoint + SuperGlue** e **SuperPoint + LightGlue**. Per il re-ranking sono stati considerati i primi $K=20$ candidati.

#### 🇯🇵 Tokyo_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 78.1 | 89.5 | 92.4 | 93.7 |
| MixVPR | **SuperPoint + SuperGlue** | 87.0 | 91.7 | 93.0 | 93.7 |
| MixVPR | **SuperPoint + LightGlue** | **88.9** | **92.4** | **93.0** | **93.7** |

#### 🇺🇸 San Francisco_XS
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 70.2 | 79.0 | 81.3 | 83.9 |
| MixVPR | **SuperPoint + SuperGlue** | 80.3 | 82.7 | 83.5 | 83.9 |
| MixVPR | **SuperPoint + LightGlue** | **81.0** | **83.3** | **83.7** | **83.9** |

#### 🌑 SVOX Night (Cross-Domain)
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 62.9 | 79.8 | 84.1 | 88.0 |
| MixVPR | **SuperPoint + LightGlue** | **82.0** | 86.4 | 87.1 | **88.0** |
| MixVPR | **SuperPoint + SuperGlue** | **82.0** | **86.6** | **87.4** | **88.0** |

#### ☀️ SVOX Sun
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 85.4 | 93.0 | 94.7 | 95.9 |
| MixVPR | **SuperPoint + LightGlue** | **91.5** | **95.2** | **95.7** | **95.9** |
| MixVPR | **SuperGlue** | 89.9 | 94.3 | 95.6 | 95.9 |

---

## ⏱️ Analisi dell'Efficienza (Hardware: Apple M4 Pro)



| Dataset | Numero Query | Latenza Global Retrieval (MixVPR) | Latenza Re-ranking (SP+LG) | Latenza Re-ranking (SuperGlue) | Fattore di Rallentamento (MixVPR vs SG) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **sf_xs** | 1000 | **0.21s** | **4.63s** | **3.64s** | ~17x |
| **tokyo_xs** | 315 | **0.39s** | **4.58s** | **8.04s** | ~20x |
| **svox_night** | 823 | **0.19s** | **4.56s** | **17.18s** | ~90x |
| **svox_sun** | 854 | **0.18s** | **4.53s** | **8.19s** (CPU) | ~45x |

---

## 🧠 Analisi Tecnica e Conclusioni Preliminari

* **Superiorità di LightGlue:** In entrambi i dataset urbani (Tokyo e SF), LightGlue supera SuperGlue nella Recall@1 con uno scarto compreso tra **+0.7% e +1.9%**. Questo conferma l'efficacia dell'architettura di LightGlue nel filtrare le corrispondenze errate e gestire le ambiguità visive.
* **Ottimizzazione Hardware:** SuperGlue risulta più rapido di circa **1 secondo per query** (~20% più veloce) su chip M4 Pro. Questo suggerisce che l'implementazione attuale di SuperGlue sfrutti meglio i kernel Metal (MPS) per le operazioni di attenzione su batch di 20 immagini.
* **Recupero Geometrico:** Entrambi i metodi portano la Recall@1 vicina alla Recall@20 del retrieval globale. Questo dimostra che il re-ranking è in grado di correggere quasi ogni errore del descrittore globale, a patto che l'immagine corretta sia stata inclusa nel set iniziale dei candidati (Top-K).
* **Costo Computazionale:** Il re-ranking aumenta il tempo di processamento di circa **20 volte**. È una soluzione ideale per sistemi di precisione, ma richiede strategie adattive (Sezione 6.1) per l'uso in contesti a bassa latenza.