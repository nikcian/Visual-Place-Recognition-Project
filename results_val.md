## San Francisco XS (Validation Subset - 1000 Query)

### 📊 Analisi Comparativa: Recall @N
| Metodo | Matcher Locale | R@1 | R@5 | R@10 | R@20 | Miglioramento R@1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| MixVPR (Baseline) | - | 86.4 | 92.8 | 94.6 | 96.1 | - |
| MixVPR | **LoFTR** | **90.0** | 94.7 | **95.9** | **96.9** | **+3.6%** |
| MixVPR | **SuperPoint + LG** | 88.7 | **95.0** | 95.8 | **96.9** | **+2.3%** |

---

### ⏱️ Analisi dell'Efficienza (Hardware: Apple M4 Pro)
| Metodo | Latenza Global | Latenza Re-ranking | Tempo Totale (1000 q) |
| :--- | :---: | :---: | :---: |
| MixVPR + **LoFTR** | 0.19s | **3.31s** | **55m 10s** |
| MixVPR + **SP-LG** | 0.19s | 4.62s | 1h 16m 59s |