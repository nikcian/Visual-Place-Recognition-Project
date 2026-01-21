# 6.7 Riassunto Generale delle Prestazioni

Di seguito riportiamo una tabella comparativa che riassume le prestazioni dei due metodi (**LoFTR** e **SuperPoint + LightGlue**) su tutti i dataset analizzati (Validazione e Test).
Le soglie ($\tau$) sono state fissate in fase di training (SVOX Sun) e mantenute costanti per tutti gli esperimenti successivi.

| Dataset | Dominio | Metodo | Tau ($\tau$) | Recall@1 | Saving | Efficienza |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SF-XS Val** | Urbano (Giorno) | **LoFTR** | 15 | 54.60% | **61.74%** | ⭐ Alta |
| | | **SP+LG** | 12 | 57.30% | 55.15% | ⭐ Alta |
| | | | | | | |
| **SVOX Sun** | Misto (Giorno) | **LoFTR** | 15 | 44.03% | 42.43% | ✅ Media |
| | | **SP+LG** | 12 | 42.86% | 46.07% | ✅ Media |
| | | | | | | |
| **SVOX Night** | Misto (Notte) | **LoFTR** | 15 | 21.26% | 10.86% | ⚠️ Bassa (Atteso) |
| | | **SP+LG** | 12 | 20.17% | 14.98% | ⚠️ Bassa (Atteso) |
| | | | | | | |
| **SF-XS Test** | Urbano (Giorno) | **LoFTR** | 15 | 28.70% | **55.25%** | ⭐ Alta |
| | | **SP+LG** | 12 | 36.50% | 36.05% | ✅ Media |
| | | | | | | |
| **Tokyo-XS** | Urbano (Giorno) | **LoFTR** | 15 | 46.98% | **52.29%** | ⭐ Alta |
| | | **SP+LG** | 12 | 46.67% | 47.51% | ✅ Media |

---

# 6.8 Conclusioni Generali e Risposta alla "Research Question"

Il progetto partiva dalla domanda fondamentale posta nell'estensione: *"Can Re-ranking be Adaptive?"* e *"How to decide the threshold?"*.
Alla luce dei risultati sperimentali ottenuti su dataset diversificati (Pittsburgh, San Francisco, Tokyo) e condizioni variabili (Giorno, Notte), possiamo trarre le seguenti conclusioni:

### 1. Efficacia della Metodologia basata su F1-Score
La strategia proposta di selezionare la soglia $\tau$ massimizzando l'**F1-Score** sul training set (classificazione Easy/Hard) si è rivelata vincente. Le soglie calcolate (**$\tau=15$ per LoFTR**, **$\tau=12$ per SP+LG**) hanno dimostrato una notevole capacità di **generalizzazione**. Nonostante siano state apprese su Pittsburgh (SVOX), hanno mantenuto prestazioni coerenti e robuste anche su domini completamente diversi come Tokyo e San Francisco, senza necessità di ri-addestramento.

### 2. Il Sistema è "Consapevole" del Contesto
L'aspetto più interessante dei risultati è l'adattabilità intrinseca del sistema:
* **Di Giorno (SVOX Sun, Tokyo, SF):** Il sistema riconosce l'alta qualità dei match e attiva il risparmio, tagliando i tempi di calcolo del **40-60%**.
* **Di Notte (SVOX Night):** Il sistema rileva automaticamente la scarsità di inlier (incertezza) e disattiva quasi completamente il risparmio (scendendo al **10-15%**).
Questo comportamento è ideale: il sistema non sacrifica la precisione quando il rischio di errore è alto, ma ottimizza aggressivamente quando le condizioni sono favorevoli.

### 3. Trade-off Recall vs. Latenza
L'Adaptive Re-ranking non è privo di costi. Come evidenziato nella discussione (Sez. 6.6), accettiamo una perdita di Recall@1 (variabile tra il 15% e il 25% rispetto al re-ranking esaustivo) in cambio di un dimezzamento dei tempi di latenza.
In applicazioni real-time (es. guida autonoma o robotica mobile), dove il budget computazionale è limitato, questa strategia offre un compromesso molto più vantaggioso rispetto al re-ranking casuale o all'assenza totale di re-ranking.

### 4. Confronto tra Metodi (LoFTR vs SP+LG)
Entrambi i metodi rispondono bene alla strategia adattiva.
* **LoFTR (Dense):** Tende ad avere un risparmio computazionale leggermente superiore e più stabile (vedi SF-XS Test), grazie alla maggiore quantità di match che genera, rendendo la soglia di 15 molto discriminante.
* **SuperPoint+LightGlue (Sparse):** Richiede una soglia più bassa ($\tau=12$) e tende ad essere leggermente più conservativo in alcuni scenari (es. SF-XS Test), ma offre prestazioni di Recall comparabili.

In conclusione, l'Adaptive Re-ranking basato su Hard-Thresholding degli inlier è una soluzione **efficace, efficiente e robusta** per scalare i sistemi di Visual Place Recognition su grandi dataset urbani.