# 6.1.1 Analisi della Selezione della Soglia: SVOX Sun Train (LoFTR)

In questa sezione determiniamo la soglia ottimale di inlier ($\tau$) per definire le "Query Difficili" (*Hard Queries*) utilizzando il dataset **SVOX Sun Train**. 

L'obiettivo è massimizzare l'equilibrio tra l'affidabilità della classificazione (**F1-Score**) e l'efficienza computazionale.

![Trade-off Recall vs Saving](grafici_tau/tau_svox_sun_train_loftr.png.png)
*Fig 6.1: Trade-off tra Recall@1 (Blu) e Risparmio Computazionale (Verde) in funzione della soglia di inlier $\tau$. La linea verticale indica la soglia ottimale.*

### Analisi dei Dati e Tabella di Trade-off

La seguente tabella illustra le prestazioni della strategia adattiva attraverso diversi livelli di soglia (con step di 5).

| Tau ($\tau$) | Recall@1 | Saving | F1-Score | Note |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 17.42% | 93.99% | 0.6809 | |
| 5 | 17.56% | 92.66% | 0.6854 | |
| 10 | 31.04% | 52.74% | 0.7050 | |
| **15** | **37.36%** | **32.91%** | **0.7273** | ⭐ **BEST** |
| 20 | 38.90% | 29.48% | 0.7220 | |
| 25 | 39.61% | 28.29% | 0.7160 | |
| 30 | 40.03% | 27.23% | 0.7086 | |
| 35 | 40.03% | 26.83% | 0.7088 | |
| 40 | 40.87% | 25.78% | 0.6904 | |
| 45 | 40.87% | 25.78% | 0.6904 | |
| 50 | 41.15% | 25.38% | 0.6834 | |
| 55 | 41.29% | 25.12% | 0.6786 | |
| 60 | 41.43% | 24.85% | 0.6739 | |
| 65 | 41.71% | 24.59% | 0.6691 | |
| 70 | 41.85% | 24.06% | 0.6594 | |
| 75 | 41.85% | 23.79% | 0.6545 | |
| 80 | 42.13% | 23.40% | 0.6471 | |
| 85 | 42.28% | 23.00% | 0.6396 | |
| 90 | 42.42% | 22.60% | 0.6320 | |
| 95 | 42.56% | 22.47% | 0.6294 | |
| 100 | 43.12% | 21.55% | 0.6151 | |

> **Nota:** Il Best Tau matematico esatto (step=1) è: **14**.

> **Nota:** Un'analisi granulare (step=1) ha identificato il massimo matematico esatto dell'F1-Score a **$\tau = 14$**.

### Metodologia: Come è stata determinata la Soglia

La selezione del $\tau$ ottimale è stata guidata dall'**F1-Score**, che agisce come media armonica tra la capacità del sistema di fidarsi dei match corretti (Precisione nell'evitare re-ranking non necessari) e la sua capacità di rilevare errori (Recall nel segnalare query difficili).

* **Soglie Basse ($\tau < 10$):**
    A soglie estremamente basse (es. $\tau=5$), il sistema classifica quasi tutte le query come "Facili" (*Easy*). Sebbene ciò produca un risparmio computazionale massiccio (>92%), la Recall@1 rimane bloccata al livello del retrieval di base (~17%). Questo indica che il sistema si sta "fidando ciecamente" di match deboli.

* **Il Punto di Gomito ("Elbow Point", $\tau \approx 15$):**
    Aumentando $\tau$ a 15, osserviamo un salto critico. La Recall@1 raddoppia (da ~17% a 37.36%) perché il sistema inizia a identificare correttamente le query "Difficili" e ad applicare il re-ranking dove necessario. L'F1-Score raggiunge qui il picco (**0.7273**), indicando che questo è il punto operativo più efficiente: risparmiamo circa il 33% del calcolo recuperando la maggior parte delle prestazioni recuperabili.

* **Soglie Alte ($\tau > 40$):**
    Oltre $\tau=40$, l'F1-Score inizia a scendere. Il guadagno in Recall rallenta significativamente (stabilizzandosi intorno al 41-43%), ma il Risparmio Computazionale continua a diminuire. Impostare una soglia così alta costringe il sistema a riordinare quasi tutto, annullando il beneficio della strategia adattiva (l'approccio Adattivo tende a diventare Re-ranking Standard).

### Conclusione per SVOX Sun (LoFTR)

Selezioniamo **$\tau = 14$** (approssimato a 15 nella tabella a step 5) come valore di taglio. Questa soglia permette a LoFTR di saltare il re-ranking per circa **un terzo delle query** (33% di risparmio) con una perdita minima di recall potenziale rispetto alla pipeline a costo pieno.