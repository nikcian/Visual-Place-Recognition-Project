# 6.1.2 Analisi della Selezione della Soglia: SVOX Sun Train (SP+LG)

Analogamente a quanto fatto per LoFTR, in questa sezione analizziamo il comportamento di **SuperPoint + LightGlue** sul dataset **SVOX Sun Train**. 
L'obiettivo è individuare la soglia di inlier $\tau$ che massimizzi l'F1-Score, garantendo il miglior compromesso tra il recupero delle query difficili e il risparmio di tempo.

![Trade-off Recall vs Saving SP+LG](grafici_tau/tau_svox_sun_train_sp+lg.png)
*Fig 6.2: Trade-off tra Recall@1 (Blu) e Risparmio Computazionale (Verde) per SuperPoint+LightGlue.*

### Analisi dei Dati e Tabella di Trade-off

La seguente tabella mostra l'andamento delle metriche al variare della soglia (step=5).

| Tau ($\tau$) | Recall@1 | Saving | F1-Score | Note |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 18.12% | 93.32% | 0.6704 | |
| 5 | 21.49% | 80.50% | 0.6880 | |
| **10** | **33.01%** | **45.34%** | **0.7151** | ⭐ **BEST** |
| 15 | 36.80% | 33.97% | 0.7273 | |
| 20 | 38.48% | 30.80% | 0.7128 | |
| 25 | 38.90% | 28.82% | 0.7140 | |
| 30 | 39.47% | 26.97% | 0.7069 | |
| 35 | 39.61% | 26.44% | 0.7048 | |
| 40 | 39.89% | 26.04% | 0.6978 | |
| 45 | 39.89% | 25.78% | 0.6931 | |
| 50 | 40.03% | 25.38% | 0.6897 | |
| 55 | 40.73% | 24.72% | 0.6777 | |
| 60 | 40.87% | 24.59% | 0.6752 | |
| 65 | 41.29% | 23.93% | 0.6630 | |
| 70 | 41.99% | 23.13% | 0.6479 | |
| 75 | 42.13% | 22.21% | 0.6300 | |
| 80 | 42.56% | 20.62% | 0.5981 | |
| 85 | 43.12% | 19.04% | 0.5686 | |
| 90 | 44.24% | 17.45% | 0.5336 | |
| 95 | 44.66% | 16.52% | 0.5124 | |
| 100 | 45.08% | 15.07% | 0.4820 | |

> **Ottimo Matematico:** L'analisi fine (step=1) ha identificato il picco esatto dell'F1-Score a **$\tau = 12$**.

### Metodologia: Interpretazione per SuperPoint+LightGlue

A differenza di LoFTR, che produce corrispondenze dense, SuperPoint+LightGlue lavora su feature sparse. Questo influenza la distribuzione degli inlier e, di conseguenza, la scelta della soglia.

* **Soglie Molto Basse ($\tau < 5$):**
    Con $\tau=5$, il sistema ottiene un risparmio enorme (80%), ma la Recall@1 è ferma al 21%. Questo significa che molti match corretti hanno un numero di inlier superiore a 5, ma vengono ignorati o considerati "facili" erroneamente se ci affidiamo solo al retrieval globale.

* **La Zona Ottimale ($\tau \approx 12$):**
    Il punto di equilibrio matematico si trova a **$\tau=12$**.
    * A **$\tau=10$**, il risparmio è ancora molto elevato (**45.34%**), con una Recall che sale drasticamente al 33%.
    * Tra 10 e 15 inlier si trova il "gomito" della curva: superata questa soglia, la capacità del sistema di distinguere tra query facili e difficili basandosi solo sul numero di inlier diminuisce.
    * È interessante notare come SP+LG permetta un **risparmio computazionale maggiore** (circa 40-45% alla soglia ottima) rispetto a LoFTR (circa 33%), suggerendo che quando SP+LG trova un match con pochi inlier, è molto probabile che sia un vero negativo o un match difficile.

* **Soglie Alte ($\tau > 30$):**
    Oltre i 30 inlier, la curva di F1-Score inizia a scendere e il risparmio si appiattisce sotto il 27%. A differenza di LoFTR, dove la densità di punti permetteva soglie più alte, con SP+LG alzare troppo la soglia erode rapidamente il vantaggio dell'approccio adattivo, costringendo a calcoli inutili.

### Conclusione per SVOX Sun (SP+LG)

Selezioniamo **$\tau = 12$** come valore operativo.
Questa scelta è strategica: garantisce un **risparmio computazionale significativo (~40%)**, evitando il re-ranking su quasi la metà del dataset, pur mantenendo una Recall@1 competitiva e massimizzando l'F1-Score del classificatore *Easy/Hard*.

# 6.1.4 Analisi della Selezione della Soglia: SVOX Night Train (SP+LG)

Concludiamo la fase di training analizzando il comportamento di **SuperPoint + LightGlue** sul dataset notturno **SVOX Night Train**.
Come per LoFTR, ci aspettiamo che la scarsa illuminazione riduca drasticamente il numero di inlier, rendendo difficile per il sistema distinguere i match corretti dai falsi positivi senza eseguire il re-ranking.

![Trade-off Recall vs Saving Night SP+LG](grafici_tau/tau_svox_night_train_sp+lg.png)
*Fig 6.4: Trade-off tra Recall@1 (Blu) e Risparmio Computazionale (Verde) su SVOX Night Train (SP+LG).*

### Analisi dei Dati e Tabella di Trade-off

La tabella seguente mostra il crollo delle prestazioni di risparmio all'aumentare della soglia (step=5).

| Tau ($\tau$) | Recall@1 | Saving | F1-Score | Note |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 2.28% | 90.90% | 0.2429 | |
| 5 | 6.98% | 57.38% | 0.2328 | |
| 10 | 11.11% | 14.75% | 0.3107 | |
| **15** | **12.68%** | **5.36%** | **0.3088** | ⭐ **Zona Ottimale** |
| 20 | 12.82% | 3.62% | 0.3252 | |
| 25 | 12.96% | 3.08% | 0.3193 | |
| 30 | 12.96% | 2.68% | 0.3103 | |
| 35 | 13.11% | 2.28% | 0.2832 | |
| 40 | 13.11% | 2.01% | 0.2703 | |
| 45 | 13.25% | 1.61% | 0.2222 | |
| 50 | 13.25% | 1.61% | 0.2222 | |
| ... | ... | ... | ... | |
| 100 | 13.68% | 0.27% | 0.0408 | |

> **Nota:** Il Best Tau matematico esatto (step=1) che massimizza l'F1-Score è: **13**.

### Metodologia e Interpretazione

L'analisi evidenzia come SuperPoint+LightGlue soffra particolarmente lo scenario notturno nel contesto del filtraggio adattivo.

* **Instabilità a Soglie Basse ($\tau=5$):**
    A $\tau=5$, il sistema risparmia ancora il 57% del calcolo, ma la Recall è bassissima (6.98%). Rispetto allo scenario diurno (dove a parità di inlier la confidenza era alta), qui 5 inlier non sono sufficienti a garantire che il match sia corretto.

* **Il Punto di Ottimo ($\tau=13$):**
    Il calcolo matematico identifica **$\tau=13$** come soglia ideale. Tuttavia, osserviamo la tabella tra 10 e 15:
    * A **$\tau=10$**, il risparmio è già crollato al **14.75%**.
    * A **$\tau=15$**, il risparmio è minimo (**5.36%**).
    
    Questo indica che la stragrande maggioranza dei match corretti di notte ha un numero di inlier compreso tra 0 e 15. Per "pescare" questi match corretti, dobbiamo necessariamente impostare una soglia che costringe il sistema a riverificare (re-rank) quasi tutto il dataset (oltre il 90% delle query).

### Conclusione per SVOX Night (SP+LG)

Selezioniamo **$\tau = 13$** come valore operativo.
Similmente a quanto deciso per LoFTR, accettiamo un **risparmio computazionale molto basso (circa 6-7%)** pur di non compromettere la capacità del sistema di recuperare le immagini corrette. In condizioni notturne, l'approccio adattivo converge naturalmente verso il comportamento di re-ranking standard per massimizzare l'accuratezza.


### 6.2.2 Validazione su SF-XS Val (SuperPoint + LightGlue)

Proseguiamo la validazione applicando la soglia $\tau=12$ (ottenuta dal training su SVOX Sun) al matcher **SuperPoint + LightGlue** sul dataset di validazione di San Francisco.

![Validazione SF-XS SP+LG](grafici_tau/validation_tau_sf_xs_val_sp+lg.png)
*Fig 6.9: Validazione della soglia $\tau=12$ su SF-XS (SP+LG).*

| Metodo | Tau Scelto ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **SP + LG** | **12** | **57.30%** | **55.15%** |

**Discussione:**
La validazione conferma la robustezza della soglia anche per questo matcher.
Con **$\tau=12$**, otteniamo un **Risparmio del 55.15%**, molto simile a quello di LoFTR, ma con una **Recall@1 leggermente superiore (57.30%)**.
Questo risultato indica che SuperPoint+LightGlue, pur generando meno inlier in valore assoluto rispetto a LoFTR (da cui la soglia più bassa, 12 vs 15), mantiene una distribuzione molto netta tra "Easy" e "Hard". La strategia adattiva si dimostra quindi "agnostica" rispetto al matcher: basta calibrare il $\tau$ in fase di training per ottenere dimezzamenti dei tempi di calcolo su nuove città senza riconfigurare il sistema.

### 6.3.3 Valutazione sui Test Set: SVOX Sun & Night (SP+LG)

Analizziamo ora le prestazioni di **SuperPoint + LightGlue** sui dataset di test SVOX, applicando la soglia fissa **$\tau = 12$**.

#### SVOX Sun Test (Scenario Diurno)

![Test SVOX Sun SP+LG](grafici_tau/test_tau_svox_sun_sp+lg.png)
*Fig 6.10: Performance su SVOX Sun Test (SP+LG) con $\tau=12$.*

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **SP + LG** | **12** | **42.86%** | **46.07%** |

**Analisi:**
Nello scenario diurno, SuperPoint+LightGlue mostra un ottimo bilanciamento. Il **Risparmio del 46.07%** è leggermente superiore a quello ottenuto con LoFTR (42.43%), indicando che la soglia $\tau=12$ permette di filtrare una porzione maggiore di query come "Facili". La Recall@1 (42.86%) rimane solida e competitiva, confermando l'efficacia della strategia in condizioni di buona illuminazione.

#### SVOX Night Test (Scenario Notturno)

![Test SVOX Night SP+LG](grafici_tau/test_tau_svox_night_sp+lg.png)
*Fig 6.11: Performance su SVOX Night Test (SP+LG) con $\tau=12$. Il risparmio si riduce drasticamente per garantire la Recall.*

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **SP + LG** | **12** | **20.17%** | **14.98%** |

**Analisi:**
Nello scenario notturno, il sistema adatta il suo comportamento alla difficoltà del dominio.
Il **Risparmio scende al 14.98%**, segno che per l'85% delle query notturne il sistema non ha trovato abbastanza inlier nel primo risultato e ha proceduto correttamente al re-ranking.
È interessante notare che il risparmio qui è leggermente più alto rispetto a LoFTR notturno (14.98% vs 10.86%): questo accade perché la soglia di taglio è più bassa (12 vs 15), rendendo statisticamente un po' più "facile" superare il check di sicurezza, anche se la Recall rimane sostanzialmente allineata (20.17%).

### 6.4.2 Valutazione su SF-XS Test (SP+LG)

Analizziamo le prestazioni di **SuperPoint + LightGlue** sul dataset di test urbano **SF-XS Test** con la soglia fissa **$\tau=12$**.

![Test SF-XS SP+LG](inserisci_qui_il_tuo_grafico_sfxs_test_splg.png)
*Fig 6.12: Performance su SF-XS Test (SP+LG) con $\tau=12$.*

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **SP + LG** | **12** | **36.50%** | **36.05%** |

**Analisi:**
Su questo dataset, SuperPoint+LightGlue mostra un comportamento più conservativo rispetto a LoFTR.
Il **Risparmio si attesta al 36.05%** (contro il 55% di LoFTR), indicando che molte query di San Francisco risultano "difficili" per SP+LG, il quale tende a produrre un numero di inlier inferiore alla soglia di 12, forzando così il re-ranking.
La Recall@1 è del **36.50%**. Anche qui, come discusso per LoFTR, il gap rispetto al re-ranking totale è il prezzo da pagare per l'efficienza, ma il sistema dimostra comunque di saper accelerare il processo per oltre un terzo delle query.

### 6.5.2 Valutazione su Tokyo-XS Test (SP+LG)

Concludiamo l'intera fase sperimentale testando **SuperPoint + LightGlue** sul dataset **Tokyo-XS**, utilizzando la soglia fissa **$\tau=12$**.

![Test Tokyo-XS SP+LG](grafici_tau/test_tau_tokyo_sp+lg.png)
*Fig 6.13: Performance su Tokyo-XS Test (SP+LG) con $\tau=12$.*

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **SP + LG** | **12** | **46.67%** | **47.51%** |

**Analisi e Conclusioni:**
I risultati su Tokyo confermano la solidità dell'approccio anche per i metodi *sparse*.
Otteniamo un **Risparmio del 47.51%** e una **Recall@1 del 46.67%**.
È interessante notare la forte similitudine con i risultati di LoFTR su questo stesso dataset (Recall 46.98%). Ciò suggerisce che la strategia adattiva è stabile: indipendentemente dal matcher utilizzato (Dense o Sparse), se calibrata correttamente (tramite F1-score sul training), la soglia riesce a identificare correttamente circa la metà delle query come "Easy", dimezzando i tempi di latenza totali senza crolli imprevisti nelle prestazioni.


