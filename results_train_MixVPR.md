## Svox-train

### Condizione night
R@1: 47.3, R@5: 64.0, R@10: 69.7, R@20: 75.8


### Condizione sun
R@1: 70.6, R@5: 82.3, R@10: 85.4, R@20: 88.2



### 📊 Risultati SVOX Train: Analisi Comparativa Finale (LoFTR)

#### 🌑 SVOX Train Night (Set Difficile / Cross-Domain)
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 | Miglioramento R@1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 47.3 | 64.0 | 69.7 | 75.8 | - |
| MixVPR | **LoFTR** | 66.7 | 72.5 | 73.9 | 75.8 | +19.4% |
| MixVPR | **SuperPoint + LG** | **66.8** | **72.9** | **74.6** | **75.8** | **+19.5%** |

#### ☀️ SVOX Train Sun (Set Facile / In-Domain)
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 | Miglioramento R@1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 70.6 | 82.3 | 85.4 | 88.2 | - |
| MixVPR | **LoFTR** | **84.6** | **87.4** | **87.9** | **88.2** | **+14.0%** |
| MixVPR | **SuperPoint + LG** | 84.1 | 87.1 | 87.9 | 88.2 | +13.5% |

### ⏱️ Analisi dell'Efficienza (Hardware: Apple M4 Pro)

| Dataset | Numero Query | Latenza Global | Latenza LoFTR | Latenza SP+LG | Tempo Totale (Full SP+LG) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **SVOX Train Night** | 702 | 0.19s | 3.26s | **4.71s** | **~55m 03s** |
| **SVOX Train Sun** | 712 | 0.19s | 3.29s | **4.80s** | **~56m 55s** |