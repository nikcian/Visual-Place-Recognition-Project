# 6.1.2 Analisi della Selezione della Soglia: SVOX Sun Train (SP+LG)

Analogamente a quanto fatto per LoFTR, in questa sezione analizziamo il comportamento di **SuperPoint + LightGlue** sul dataset **SVOX Sun Train**. 
L'obiettivo è individuare la soglia di inlier $\tau$ che massimizzi l'F2-Score, garantendo il miglior compromesso tra il recupero delle query difficili e il risparmio di tempo.

![Trade-off Recall vs Saving SP+LG Sun](/plots/Hard%20Thresholding/NETVLAD/tau_svox_sun_train_sp+lg.png)
*Fig 6.2: Trade-off tra Recall@1 (Blu) e Risparmio Computazionale (Verde) per SuperPoint+LightGlue su SVOX Sun.*

### Analisi dei Dati e Tabella di Trade-off

La seguente tabella mostra l'andamento delle metriche al variare della soglia.

| Tau | Recall | Saving | F2-Score | Note |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 29.92% | 99.16% | 0.3477 | |
| 5 | 33.15% | 85.53% | 0.3777 | |
| **10** | **44.24%** | **48.17%** | **0.4498** | **⭐ BEST** |
| 15 | 47.61% | 36.10% | 0.4476 | |
| 20 | 49.16% | 32.72% | 0.4467 | |
| 25 | 49.44% | 30.62% | 0.4403 | |
| 30 | 50.00% | 28.65% | 0.4352 | |
| 35 | 50.00% | 28.09% | 0.4325 | |
| 40 | 50.14% | 27.67% | 0.4313 | |
| 45 | 50.14% | 27.39% | 0.4300 | |
| 50 | 50.14% | 26.97% | 0.4279 | |
| 55 | 50.28% | 26.26% | 0.4251 | |
| 60 | 50.28% | 26.12% | 0.4243 | |
| 65 | 50.42% | 25.42% | 0.4213 | |
| 70 | 50.56% | 24.58% | 0.4174 | |
| 75 | 50.56% | 23.60% | 0.4115 | |
| 80 | 50.56% | 21.91% | 0.4008 | |
| 85 | 50.42% | 20.22% | 0.3883 | |
| 90 | 50.42% | 18.54% | 0.3752 | |
| 95 | 50.42% | 17.56% | 0.3669 | |
| 100 | 50.42% | 16.01% | 0.3526 | |

### Metodologia: Interpretazione per SuperPoint+LightGlue

A differenza di LoFTR, che produce corrispondenze dense, SuperPoint+LightGlue lavora su feature sparse. Tuttavia, l'analisi mostra una convergenza notevole verso valori simili.

* **La Zona Ottimale ($\tau = 10$):**
    Il picco matematico dell'F2-Score si trova esattamente a **$\tau=10$**.
    A questa soglia, otteniamo un ottimo **Risparmio del 48.17%** con una Recall del **44.24%**.
    Superare questa soglia (es. $\tau=15$) porta a un guadagno marginale di Recall (+3%) ma a un costo significativo in termini di efficienza (-12% di risparmio), rendendo il sistema meno attraente per applicazioni real-time.

### Conclusione per SVOX Sun (SP+LG)

Selezioniamo **$\tau = 10$** come valore operativo ideale per lo scenario diurno.

---

# 6.1.4 Analisi della Selezione della Soglia: SVOX Night Train (SP+LG)

Concludiamo la fase di training analizzando il comportamento sul dataset notturno **SVOX Night Train**.

![Trade-off Recall vs Saving Night SP+LG](/plots/Hard%20Thresholding/NETVLAD/tau_svox_night_train_sp+lg.png)
*Fig 6.4: Trade-off su SVOX Night Train (SP+LG).*

### Analisi dei Dati e Tabella di Trade-off

| Tau | Recall | Saving | F2-Score | Note |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 3.42% | 96.58% | 0.0424 | |
| 5 | 7.98% | 60.97% | 0.0966 | |
| **9** | **11.82%** | **20.23%** | **0.1289** | **⭐ BEST** |
| 10 | 11.97% | 15.67% | 0.1256 | |
| 15 | 13.53% | 5.70% | 0.1061 | |
| 20 | 13.68% | 3.85% | 0.0905 | |
| 25 | 13.82% | 3.28% | 0.0841 | |
| 30 | 13.82% | 2.85% | 0.0781 | |
| 35 | 13.82% | 2.42% | 0.0712 | |
| 40 | 13.68% | 2.14% | 0.0657 | |
| 45 | 13.68% | 1.71% | 0.0570 | |
| 50 | 13.68% | 1.71% | 0.0570 | |
| 55 | 13.68% | 1.71% | 0.0570 | |
| 60 | 13.68% | 1.57% | 0.0537 | |
| 65 | 13.68% | 1.14% | 0.0427 | |
| 70 | 13.68% | 1.00% | 0.0386 | |
| 75 | 13.68% | 0.85% | 0.0342 | |
| 80 | 13.68% | 0.71% | 0.0295 | |
| 85 | 13.68% | 0.57% | 0.0244 | |
| 90 | 13.68% | 0.43% | 0.0190 | |
| 95 | 13.68% | 0.43% | 0.0190 | |
| 100 | 13.68% | 0.28% | 0.0131 | |

### Metodologia e Interpretazione

L'analisi notturna conferma la difficoltà del dominio:
* **Il Punto di Ottimo ($\tau=9$):**
    L'analisi matematica suggerisce **$\tau=9$** come miglior compromesso. Tuttavia, la differenza con **$\tau=10$** è minima in termini di score, ma a 10 otteniamo una Recall leggermente superiore (11.97% vs 11.82%).
* **Crollo del Risparmio:**
    Come per LoFTR, anche per SP+LG il risparmio crolla drasticamente appena si cerca di aumentare la Recall. Già a $\tau=10$, il risparmio è ridotto al **15.67%**, segno che il sistema sta re-rankando l'85% delle query per compensare l'incertezza del retrieval globale.

**Sintesi della Scelta Operativa ($\tau_{final}$):**
Considerando che l'ottimo per il giorno è **10** e l'ottimo per la notte è **9**, adottiamo **$\tau = 10$** come **soglia globale unica**. È una scelta conservativa che massimizza le prestazioni diurne e protegge quelle notturne senza richiedere parametri specifici per il dominio.

---

# 6.2.2 Validazione su SF-XS Val (SuperPoint + LightGlue)

Proseguiamo la validazione applicando la soglia scelta **$\tau=10$** al matcher **SuperPoint + LightGlue** sul dataset di validazione di San Francisco.

![Validazione SF-XS SP+LG](/plots/Hard%20Thresholding/NETVLAD/validation_tau_sf_xs_val_sp+lg.png)

| Metodo | Tau Scelto ($\tau$) | Recall@1 | Risparmio (Saving) | Note |
| :--- | :--- | :--- | :--- | :--- |
| **SP + LG** | **10** | **60.80%** | **62.80%** | ⬅️ **CHOSEN** |

**Discussione:**
La validazione è un successo. Con **$\tau=10$**, otteniamo un **Risparmio del 62.80%** con una Recall solida del **60.80%**.
Questo conferma che la soglia di 10 inlier è robusta anche per metodi *sparse*: a San Francisco, quasi il 60% delle query viene risolto correttamente dal Global Retrieval e validato geometricamente senza bisogno di re-ranking.

---

# 6.3.3 Valutazione sui Test Set: SVOX Sun & Night (SP+LG)

Analizziamo ora le prestazioni di **SuperPoint + LightGlue** sui dataset di test SVOX, applicando la soglia fissa **$\tau = 10$**.

### SVOX Sun Test

![Test SVOX Sun SP+LG](/plots/Hard%20Thresholding/NETVLAD/test_tau_svox_sun_sp+lg.png)

| Tau | Recall | Saving | F2-Score | Note |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 35.60% | 99.53% | 0.4084 | |
| 5 | 40.16% | 86.89% | 0.4500 | |
| **10** | **53.04%** | **54.57%** | **0.5334** | **⬅️ CHOSEN** |
| 15 | 57.14% | 44.61% | 0.5410 | |
| 20 | 59.13% | 39.70% | 0.5386 | |
| 25 | 59.84% | 38.41% | 0.5383 | |
| 30 | 60.66% | 36.42% | 0.5353 | |
| 35 | 61.24% | 34.89% | 0.5321 | |
| 40 | 61.36% | 33.96% | 0.5283 | |
| 45 | 61.48% | 33.02% | 0.5244 | |
| 50 | 61.71% | 32.08% | 0.5209 | |
| 55 | 61.71% | 31.50% | 0.5178 | |
| 60 | 61.71% | 30.33% | 0.5113 | |
| 65 | 61.71% | 29.27% | 0.5052 | |
| 70 | 61.59% | 28.81% | 0.5017 | |
| 75 | 61.71% | 27.87% | 0.4965 | |
| 80 | 61.71% | 26.70% | 0.4889 | |
| 85 | 61.71% | 25.29% | 0.4791 | |
| 90 | 61.71% | 24.36% | 0.4722 | |
| 95 | 61.71% | 22.95% | 0.4613 | |
| 100 | 61.71% | 21.31% | 0.4475 | |

**Analisi:**
Risultato eccellente di giorno: **Risparmio > 54.57%** e Recall del **53.04%**. Il sistema dimezza i tempi di calcolo mantenendo un'alta affidabilità. Rispetto al training, le performance sono addirittura migliorate, confermando la generalizzabilità della soglia.

### SVOX Night Test

![Test SVOX Night SP+LG](/plots/Hard%20Thresholding/NETVLAD/test_tau_svox_night_sp+lg.png)

| Tau | Recall | Saving | F2-Score | Note |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 8.63% | 94.78% | 0.1054 | |
| 5 | 13.85% | 64.52% | 0.1643 | |
| **10** | **22.72%** | **20.53%** | **0.2225** | **⬅️ CHOSEN** |
| 15 | 24.42% | 11.06% | 0.1967 | |
| 20 | 24.79% | 8.14% | 0.1759 | |
| 25 | 25.15% | 7.53% | 0.1714 | |
| 30 | 25.27% | 7.05% | 0.1666 | |
| 35 | 25.27% | 6.93% | 0.1652 | |
| 40 | 25.27% | 6.68% | 0.1624 | |
| 45 | 25.27% | 6.56% | 0.1609 | |
| 50 | 25.27% | 6.44% | 0.1595 | |
| 55 | 25.39% | 5.95% | 0.1536 | |
| 60 | 25.39% | 5.59% | 0.1486 | |
| 65 | 25.39% | 5.47% | 0.1469 | |
| 70 | 25.39% | 5.22% | 0.1433 | |
| 75 | 25.39% | 4.86% | 0.1376 | |
| 80 | 25.39% | 4.74% | 0.1357 | |
| 85 | 25.39% | 3.89% | 0.1206 | |
| 90 | 25.39% | 3.77% | 0.1182 | |
| 95 | 25.39% | 3.40% | 0.1108 | |
| 100 | 25.39% | 3.04% | 0.1027 | |

**Analisi:**
Di notte, il sistema reagisce correttamente alla difficoltà. Il risparmio scende al **20.53%**, attivando il re-ranking per l'80% delle query. Questo permette di mantenere una Recall del **22.72%**, evitando il crollo delle prestazioni che si avrebbe con una strategia di risparmio più aggressiva.

---

# 6.4.2 Valutazione su SF-XS Test (SP+LG)

Analizziamo le prestazioni sul dataset di test urbano **SF-XS Test** con $\tau=10$.

![Test SF-XS SP+LG](/plots/Hard%20Thresholding/NETVLAD/test_tau_sf_xs_sp+lg.png)

| Tau | Recall | Saving | F2-Score | Note |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 27.80% | 98.60% | 0.3246 | |
| 5 | 34.50% | 80.20% | 0.3894 | |
| **10** | **47.20%** | **44.00%** | **0.4652** | **⬅️ CHOSEN** |
| 15 | 51.70% | 33.00% | 0.4644 | |
| 20 | 52.60% | 29.20% | 0.4533 | |
| 25 | 52.90% | 27.30% | 0.4455 | |
| 30 | 53.00% | 26.00% | 0.4389 | |
| 35 | 53.10% | 25.00% | 0.4335 | |
| 40 | 53.30% | 23.50% | 0.4252 | |
| 45 | 53.40% | 22.50% | 0.4189 | |
| 50 | 53.50% | 21.60% | 0.4130 | |
| 55 | 53.50% | 20.70% | 0.4063 | |
| 60 | 53.50% | 20.40% | 0.4039 | |
| 65 | 53.30% | 19.20% | 0.3933 | |
| 70 | 53.40% | 18.40% | 0.3868 | |
| 75 | 53.40% | 17.60% | 0.3796 | |
| 80 | 53.40% | 16.20% | 0.3659 | |
| 85 | 53.40% | 15.60% | 0.3597 | |
| 90 | 53.40% | 14.60% | 0.3487 | |
| 95 | 53.40% | 13.50% | 0.3356 | |
| 100 | 53.30% | 12.10% | 0.3171 | |

**Analisi:**
Su SF-XS Test, otteniamo un buon bilanciamento: **Risparmio del 44%** e Recall del **47.20%**. Sebbene leggermente inferiore rispetto ai risultati di validazione, il sistema continua a garantire un risparmio significativo di risorse.

---

# 6.5.2 Valutazione su Tokyo-XS Test (SP+LG)

Concludiamo l'intera fase sperimentale testando **SuperPoint + LightGlue** sul dataset **Tokyo-XS**.

![Test Tokyo-XS SP+LG](/plots/Hard%20Thresholding/NETVLAD/test_tau_tokyo_sp+lg.png)

| Tau | Recall | Saving | F2-Score | Note |
| :---: | :---: | :---: | :---: | :--- |
| 0 | 50.48% | 97.78% | 0.5588 | |
| 5 | 57.14% | 77.78% | 0.6034 | |
| **10** | **64.44%** | **53.65%** | **0.6195** | **⬅️ CHOSEN** |
| 15 | 66.98% | 47.30% | 0.6184 | |
| 20 | 67.62% | 46.03% | 0.6182 | |
| 25 | 67.94% | 44.44% | 0.6144 | |
| 30 | 68.25% | 42.86% | 0.6102 | |
| 35 | 68.25% | 40.95% | 0.6022 | |
| 40 | 68.25% | 40.00% | 0.5981 | |
| 45 | 68.25% | 37.78% | 0.5877 | |
| 50 | 68.25% | 34.92% | 0.5731 | |
| 55 | 68.25% | 33.33% | 0.5643 | |
| 60 | 68.25% | 31.43% | 0.5530 | |
| 65 | 68.25% | 29.52% | 0.5407 | |
| 70 | 68.25% | 26.98% | 0.5227 | |
| 75 | 68.25% | 24.44% | 0.5024 | |
| 80 | 68.25% | 22.86% | 0.4885 | |
| 85 | 68.25% | 20.63% | 0.4670 | |
| 90 | 68.25% | 19.37% | 0.4535 | |
| 95 | 68.25% | 18.10% | 0.4391 | |
| 100 | 68.25% | 17.14% | 0.4276 | |

**Analisi e Conclusioni:**
Tokyo conferma la solidità dell'approccio. Otteniamo un **Risparmio del 53.65%** e una **Recall molto alta del 64.44%**.
Questo risultato è particolarmente significativo perché dimostra che la soglia $\tau=10$ funziona trasversalmente a diversi continenti e tipi di architettura urbana, garantendo sempre un risparmio di tempo intorno al 50% per i metodi *sparse*.

---

## 6.6 Conclusioni Finali (SuperPoint + LightGlue)

La tabella riassume l'impatto della strategia adattiva con **$\tau=10$**.

| Dataset | Adaptive Recall@1 | Risparmio Tempo | Note |
| :--- | :--- | :--- | :--- |
| **SVOX Sun** | 53.04% | **54.57%** | Dimezzamento latenza |
| **Tokyo-XS** | 64.44% | **53.65%** | Ottimo bilanciamento |
| **SF-XS Test** | 47.20% | **44%** | Efficienza solida |
| **SVOX Night** | 22.72% | **20.53%** | Priorità alla Recall |

**Sintesi:**
L'approccio adattivo con SuperPoint+LightGlue e soglia fissa a 10 si rivela una strategia vincente. Garantisce un risparmio medio del **50%** in scenari diurni/urbani, mantenendo la flessibilità necessaria per affrontare scenari notturni complessi senza intervento manuale.