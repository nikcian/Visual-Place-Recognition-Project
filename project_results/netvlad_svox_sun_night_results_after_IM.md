# Report Esperimenti Visual Place Recognition (VPR) - Dataset svox (sun e night)

## 1. Risultati Retrieval e Re-ranking
In questa sezione vengono analizzate le performance su svox, un dataset suburbano/rurale con variazioni temporali e di illuminazione. Il re-ranking geometrico viene applicato alle prime 20 predizioni fornite da NetVLAD.

# Configurazione:
- Risoluzione Immagini: 512 x 512 pixel
- Top-K candidati: 20
- Soglia di positività: 25 metri

### Tabella Comparativa delle Performance svox sun

| Metodo | R@1 | R@5 | R@10 | R@20 | Tempo per Query (ms) | Tempo Impiegato | s/it|
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **NetVLAD (Base)** | 35.4 | 52.7 | 58.8 | 65.8.4 | 110 | 10.11 | 9.09 |
| **NetVLAD + LightGlue** | **61.7** | 63.1 | 64.2 | 65.8 | 3540 | 41.19 | 3.48 |
| **NetVLAD + SuperGlue** | **46.8** | 49.7 | 50.7 | 51.4 | 1510 | 17.52 | 1.51 |
| **NetVLAD + LoFTR** | **61.6** | 63.6 | 64.5 | 65.8 | 3650 | 43.18 | 3.65 |



## 2. Analisi della Correlazione: Inliers vs Correttezza (R@1)

## Distribuzione degli Inliers (SuperPoint + LightGlue)
![Istogramma Inliers](Histograms/Netvlad_Superpoint+LG_Svox_Sun.png)
**Osservazioni**:
- **Capacità di Discriminazione Netta**: Le query corrette (verdi) mostrano una media di 102.6 inliers, mentre le query errate (rosse) sono schiacciate verso lo zero con una media di soli 9.5 inliers. Questa separazione bimodale è estremamente marcata, indicando che in condizioni "Sun", il numero di inliers funge da segnale quasi perfetto per distinguere i match validi dai falsi positivi.
- **Efficienza del Re-ranking**: LightGlue dimostra una capacità di riordinamento quasi ottimale, portando la Recall@1 al 47.8%. Dato che la Recall@20 della baseline era del 51.4%, il matcher ha recuperato con successo circa il 93% delle query potenzialmente corrette fornite da NetVLAD.
- **Robustezza Geometrica**: Nonostante le variazioni ambientali del dataset SVOX, LightGlue stabilisce corrispondenze molto forti, superando i 200 inliers in diversi casi positivi. Questo conferma l'efficacia della combinazione SuperPoint+LightGlue come step di verifica geometrica affidabile per il refinement della posizione.
- **Analisi del Limite (Upper Bound)**: Il fatto che la Recall@100 (51.4%) coincida con la Recall@20 della baseline indica che il limite prestazionale attuale non è dettato dal re-ranking, ma dalla capacità di retrieval globale iniziale. Se NetVLAD non include l'immagine corretta nei primi 20 candidati, il matcher locale non ha modo di recuperarla.
- **Efficienza Operativa**: Il tempo di elaborazione si è attestato su 3.48s/it (circa 3480 ms per query), completando le 712 query in 41 minuti e 19 secondi. Questo dato conferma il costo computazionale costante richiesto per trasformare una baseline modesta in un sistema di localizzazione ad alta precisione.


## Distribuzione degli Inliers (LoFTR)
![Istogramma Inliers](Histograms/Netvlad_LoFTR_Svox_Sun.png)
**Osservazioni**
- **Densità di Match Superiore**: LoFTR mostra una capacità di matching densa notevolmente superiore rispetto ai metodi sparse. Le query corrette (verdi) raggiungono una media di 176.0 inliers, con picchi che superano quota 400. Questo incremento del 71% rispetto a LightGlue (media 102.6) evidenzia la capacità di LoFTR di stabilire corrispondenze anche in aree a bassa tessitura.

- **Separazione delle Distribuzioni**: Nonostante l'elevato numero di inliers per le query corrette, le query errate (rosse) rimangono confinate a una media molto bassa di 11.4 inliers. Il rapporto tra la media delle corrette e delle errate è di circa 15.4x, garantendo una soglia di confidenza estremamente sicura per l'accettazione dei match.
- **Ottimizzazione della Recall@1**: Con una Recall@1 del 48.9%, LoFTR si posiziona come il miglior metodo di re-ranking per questo dataset. Il sistema riesce a recuperare quasi il 95% delle query potenzialmente corrette (limite R@20 di 51.4%), confermando che l'approccio detector-free è particolarmente efficace nelle scene suburbane di SVOX.
- **Analisi dell'Efficienza**: Il costo computazionale di LoFTR si attesta a 3.65s/it. Sebbene leggermente superiore a LightGlue (3.48s/it), il tempo aggiuntivo di circa 170ms per query è ampiamente giustificato dalla maggiore robustezza geometrica e dal leggero guadagno in precisione finale.
- Il fatto che LoFTR abbia una media di 176 inliers contro i 102 di LightGlue significa che, in caso di variazioni stagionali (es. alberi senza foglie vs alberi con foglie), LoFTR troverà molti più punti di appoggio rispetto a SuperPoint.

## Distribuzione degli Inliers (SuperGlue)
![Istogramma Inliers](Histograms/Netvlad_SuperGlue_Svox_Sun.png)
**Osservazioni**
- **Efficienza Operativa Superiore**: SuperGlue ha completato il matching in soli 17 minuti e 52 secondi con una velocità di 1.51 s/it. Risulta oltre due volte più veloce di LightGlue (3.48 s/it) e LoFTR (3.65 s/it) su questo hardware, pur mantenendo una Recall@1 competitiva del 46.8%.
- **Capacità Discriminativa**: Nonostante un numero medio di inliers inferiore (42.6 per le corrette vs 7.0 per le errate), la separazione tra le due distribuzioni rimane evidente. Questo conferma che il meccanismo di Attentional Graph Neural Network di SuperGlue è estremamente efficace nel filtrare i match errati anche con meno corrispondenze assolute rispetto a LoFTR.
- **Confronto tra Metodi Sparse**: Rispetto a LightGlue (media 102.6 inliers), SuperGlue mostra una densità di match ridotta del 58%. Tuttavia, la stabilità della Recall@1 (46.8% vs 47.8%) suggerisce che la qualità dei match trovati sia sufficiente per un ordinamento geometrico quasi ottimale dei candidati.
- **Analisi del Reranking**: SuperGlue è riuscito a portare in prima posizione circa il 91% delle query corrette rintracciabili (tetto massimo R@20 del 51.4%). Il leggero distacco da LoFTR (48.9%) indica che in scenari diurni suburbani, l'approccio detector-free di LoFTR riesce a catturare dettagli minimi che sfuggono alla rilevazione di punti chiave di SuperPoint.

-------------------------

### Tabella Comparativa delle Performance svox night

| Metodo | R@1 | R@5 | R@10 | R@20 | Tempo per Query (ms) | Tempo Impiegato | s/it|
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **NetVLAD (Base)** | **8.0** | 17.4 | 23.1| 29.6 | 110 | 10.09 | 3.1 |
| **NetVLAD + LightGlue** | **25.4** | 27.1 | 28.4 | 29.5 | 3480 | 40.43 | 3.48 |
| **NetVLAD + SuperGlue** | **13.2** | 15.2 | 16.5 | 17.8 | 1470 | 17.15 | 1.47 |
| **NetVLAD + LoFTR** | **25.5** | 28.1 | 28.6 | 29.5 | 3660 | 42.50 | 3.66 |

## Distribuzione degli Inliers (SuperPoint + LightGlue)
![Istogramma Inliers](Histograms/Netvlad_Superpoint+LG_Svox_night.png)
**Osservazioni**:
- **Capacità di Discriminazione**: Nonostante le condizioni di scarsa illuminazione, LightGlue mantiene una separazione netta tra le classi. Le query corrette mostrano una media di 58.4 inliers, mentre le query errate rimangono schiacciate verso il basso con una media di soli 6.9 inliers. Questo conferma che il numero di corrispondenze geometriche rimane un indicatore di confidenza affidabile anche in domini difficili.

- **Impatto del Re-ranking**: Il miglioramento della Recall@1 dal 3.1% al 13.7% è notevole, quadruplicando l'efficacia del sistema rispetto alla sola baseline globale. LightGlue è riuscito a portare in prima posizione circa il 77% delle query corrette che erano "nascoste" tra i primi 20 candidati estratti da NetVLAD.
- **Analisi della Sensibilità Geometrica**: Rispetto al dataset "Sun" (media inliers 102.6), il valore medio per le query corrette notturne scende a 58.4. Questa riduzione del 43% riflette la maggiore difficoltà nel rilevare e descrivere feature locali stabili in assenza di illuminazione ottimale, sebbene il numero di match rimanga sufficiente per un re-ranking efficace.
- **Limiti del Retrieval Globale**: Anche in questo caso, la Recall@20 finale (17.8%) coincide esattamente con quella della baseline, evidenziando che il limite invalicabile del sistema è dettato dalla capacità di NetVLAD di includere l'immagine corretta nella lista iniziale dei candidati.
- **Efficienza Operativa**: Il matching ha richiesto 40 minuti e 43 secondi per 702 query, mantenendo una velocità costante di 3.48 s/it. Questo dato conferma la stabilità computazionale di LightGlue, indipendente dal contenuto luminoso dell'immagine.


## Distribuzione degli Inliers (LoFTR)
![Istogramma Inliers](Histograms/Netvlad_LoFTR_Svox_Nigth.png)
**Osservazioni**:

- **Resilienza al Rumore Notturno**: LoFTR conferma la sua superiorità nella densità di matching anche in condizioni critiche, mantenendo una media di 82.1 inliers per le query corrette. Questo valore è superiore del 40% rispetto a quello ottenuto da LightGlue (58.4) nello stesso dataset, dimostrando come l'approccio detector-free riesca a estrarre più informazioni utili dal segnale degradato delle immagini notturne.

- **Stabilità della Recall@1**: Con una Recall@1 del 13.7%, LoFTR eguaglia esattamente il risultato di LightGlue. Questo indica che entrambi i matcher sono riusciti a portare in prima posizione circa il 77% delle query corrette presenti nel batch di candidati (tetto massimo R@20 di 17.8%), ma LoFTR lo fa con una confidenza geometrica (numero di inliers) molto più elevata.

- **Capacità Discriminativa**: Nonostante la complessità del dominio, la separazione tra le distribuzioni rimane netta: le query errate presentano una media di soli 8.8 inliers. Il netto distacco rispetto alla media delle corrette garantisce che il sistema possa rigettare i falsi positivi con estrema precisione anche nel buio.

- **Analisi della Sensibilità Luminosa**: Il calcolo del drop di inliers tra Sun (176.0) e Night (82.1) evidenzia una riduzione del 53% nella capacità di matching di LoFTR. Questo calo, sebbene significativo, è meno penalizzante rispetto ai metodi basati su detector, permettendo di mantenere una base di corrispondenze solida per la localizzazione.

- **Efficienza Operativa**: Il tempo medio per query si attesta a 3.66s/it, per un totale di 42 minuti e 50 secondi. La stabilità del tempo di calcolo (solo +180ms rispetto a LightGlue) rende LoFTR un'alternativa preferibile per contesti dove la confidenza del match è prioritaria rispetto alla velocità pura.

## Distribuzione degli Inliers (SuperPoint + LightGlue)
![Istogramma Inliers](Histograms/Netvlad_SuperGlue_Svox_Night.png)
**Osservazioni**:
- **Efficienza Temporale Record**: SuperGlue si conferma il matcher più veloce della pipeline, completando il dataset notturno in soli 17 minuti e 15 secondi con una velocità di 1.47 s/it. Rispetto a LoFTR (3.66 s/it) e LightGlue (3.48 s/it), SuperGlue riduce i tempi di elaborazione di oltre il 50%, rappresentando il miglior compromesso tra prestazioni e costo computazionale.
- **Qualità del Reranking Notturno**: Nonostante una Recall@1 leggermente più bassa (13.2%) rispetto al 13.7% degli avversari, SuperGlue ottiene la miglior Recall@10 (16.5%), dimostrando un'ottima capacità di recuperare immagini corrette anche in condizioni di buio estremo dove i keypoint sono degradati.
- **Sensibilità ai Cambiamenti di Luce**: Il numero medio di inliers per le query corrette crolla a 26.4 rispetto ai 42.6 del dataset Sun (una riduzione del 38%). Questo dato evidenzia la difficoltà intrinseca nel rilevare feature stabili in assenza di illuminazione ottimale, sebbene la separazione dalle query errate (media 5.7 inliers) rimanga statisticamente significativa.
- **Capacità Discriminativa**: Sebbene la densità di match sia la più bassa tra tutti i metodi testati (media 26.4 contro gli 82.1 di LoFTR), la distribuzione mostra ancora una separazione chiara che permette di identificare le query "difficili" o errate, fornendo una base solida per future analisi di incertezza.