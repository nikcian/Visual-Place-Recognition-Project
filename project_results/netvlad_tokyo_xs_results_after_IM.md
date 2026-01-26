# Report Esperimenti Visual Place Recognition (VPR) - Dataset tokyo_xs

## 1. Risultati Retrieval e Re-ranking
In questa sezione vengono analizzate le performance su tokyo_xs, un dataset caratterizzato da un'elevata densità urbana e fenomeni di perceptual aliasing (edifici visivamente simili in luoghi diversi). Il re-ranking geometrico viene applicato alle prime 20 predizioni fornite da NetVLAD.

# Configurazione:
- Risoluzione Immagini: 512 x 512 pixel
- Top-K candidati: 20
- Soglia di positività: 25 metri

### Tabella Comparativa delle Performance

| Metodo | R@1 | R@5 | R@10 | R@20 | Tempo per Query (ms) | Tempo Impiegato | s/it|
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **NetVLAD (Base)** | 49.8 | 62.5 | 70.5 | 78.7 | <100 | | |
| **NetVLAD + LightGlue** | **68.3** | 72.1 | 73.7 | 78.7 | 3540 | 18.35 | 3.54 |
| **NetVLAD + SuperGlue** | **69.5** | 72.7 | 74.9 | 78.7 | 1390 | 7.42 | 1.47 |
| **NetVLAD + LoFTR** | **68.3** | 72.7 | 73.7 | 78.7 | 3720 | 19.41 | 3.75 |


---

## 2. Analisi della Correlazione: Inliers vs Correttezza (R@1)

## Distribuzione degli Inliers (SuperPoint + LightGlue)
![Istogramma Inliers](Histograms/Netvlad_Superpoint+LG_tokyo.png)

**Osservazioni:**
- **Eccezionale Densità di Corrispondenze**: Le query corrette (verdi) mostrano una media di ben 79.5 inliers. Questo valore è significativamente alto e suggerisce che le strutture urbane di Tokyo offrono una ricchezza di texture e dettagli geometrici che SuperPoint riesce a sfruttare efficacemente.
- **Separazione Netta**: Le query errate (rosse) rimangono confinate a una media di appena 7.0 inliers. La quasi totale assenza di sovrapposizione tra le due distribuzioni indica che la verifica geometrica è un filtro quasi infallibile per questo dataset.
- **Potere Discriminante**: Impostando una soglia di confidenza (es. 20-25 inliers), è possibile distinguere con estrema precisione una corrispondenza reale da un falso positivo causato dall'aliasing visivo.


## Distribuzione degli Inliers (LoFTR)
![Istogramma Inliers](Histograms/Netvlad_LoFTR_tokyo.png)

**Osservazioni:**
- **Densità di Corrispondenze Massiva**: Le query corrette (verdi) mostrano una media impressionante di 161.9 inliers. Questo valore è più del doppio rispetto a quello ottenuto da LightGlue (79.5) sullo stesso dataset, confermando la capacità di LoFTR di stabilire match densi anche in aree urbane con geometrie complesse e ripetitive.
- **Separazione Netta e Affidabilità**: Nonostante l'elevato numero di match nelle query corrette, le query errate (rosse) rimangono confinate a una media di soli 12.2 inliers. Questo crea una finestra di separazione estremamente ampia, rendendo quasi impossibile confondere una query corretta con una errata.
- **Proxy di Reliability Superiore**: La distribuzione verde è molto estesa, arrivando a superare i 500 inliers in alcuni casi. Questa abbondanza di dati geometrici rende il sistema estremamente robusto contro le sfide tipiche di Tokyo, come le variazioni di prospettiva e il perceptual aliasing.
- **Confronto Metodologico**: Mentre LightGlue si basa su punti chiave isolati (SuperPoint), LoFTR opera a livello globale sull'immagine. Questo spiega perché, a parità di Recall@1 (68.3%), LoFTR fornisca una "confidenza" geometrica (espressa in numero di inliers) molto più elevata.


## Distribuzione degli Inliers (SuperGlue)
![Istogramma Inliers](Histograms/Netvlad_SuperGlue_tokyo.png)

**Osservazioni:**
- **Efficacia Superiore nel Reranking**: SuperGlue ottiene il miglior risultato di Recall@1 finora registrato su Tokyo_XS (69.5%). Questo suggerisce che il meccanismo di attenzione (self e cross-attention) del modello permette di scartare con maggiore precisione i falsi positivi prodotti da NetVLAD.
- **Distribuzione degli Inliers**: Le query corrette (verdi) mostrano una media di 23.3 inliers. Sebbene numericamente inferiore rispetto a LoFTR (161.9) o LightGlue (79.5), la qualità di questi match è estremamente alta, come dimostrato dalle performance di Recall superiori.
- **Capacità Discriminante**: Le query errate (rosse) sono fortemente concentrate in un range molto stretto, con una media di soli 5.4 inliers. La quasi totale assenza di query errate sopra i 15 inliers conferma che SuperGlue è un indicatore di affidabilità (proxy di reliability) estremamente preciso: un punteggio basso è quasi sempre sinonimo di errore.
- **Ottimizzazione del Trade-off**: Si conferma che SuperGlue offre un equilibrio ideale tra densità di informazione e precisione. Anche con un numero di inliers contenuto, la struttura geometrica identificata è sufficientemente robusta da superare le sfide del perceptual aliasing tipiche dell'ambiente urbano giapponese.
