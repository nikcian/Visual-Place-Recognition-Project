# Report Esperimenti Visual Place Recognition (VPR) - Dataset sf_xs

## 1. Risultati Retrieval e Re-ranking
In questa sezione vengono confrontate le performance del metodo di retrieval (NetVLAD) con l'applicazione di algoritmi di Image Matching per il re-ranking delle prime 20 predizioni.

**Configurazione:**
- **Risoluzione Immagini:** 512 x 512 pixel (per Image Matching)
- **Top-K candidati:** 20
- **Soglia di positività:** 25 metri

### Tabella Comparativa delle Performance

| Metodo | R@1 | R@5 | R@10 | R@20 | Tempo per Query (ms) | Tempo Impiegato | s/it|
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **NetVLAD (Base)** | 27.2 | 43.8 | 50.3 | 56.2 | <100 | 2.58 | |
| **NetVLAD + LightGlue** | **53.2** | 55.4 | 55.8 | 56.2 | 3170 | 52.51 | 3.17 |
| **NetVLAD + SuperGlue** | **52.4** | 55.3 | 55.8 | 56.2 | 1390 | 23.16 | 1.40 |
| **NetVLAD + LoFTR** | **53.6** | 55.3 | 55.8 | 56.2 | 3500 | 59.39 | 3.58 |

---

## 2. Analisi della Correlazione: Inliers vs Correttezza (R@1)
L'obiettivo di questa analisi è verificare se il numero di inliers (punti di corrispondenza validi) trovati dal matcher possa fungere da indicatore di confidenza per distinguere tra una predizione corretta e una errata.

### Distribuzione degli Inliers (SuperPoint + LightGlue)
![Istogramma Inliers](Histograms/Netvlad_Superpoint+LG.png)

**Osservazioni:**
- **Separazione delle Distribuzioni:** Le query corrette (verdi) mostrano una distribuzione chiaramente spostata verso valori alti di inliers (Media: 100.6), mentre le query errate (rosse) si concentrano quasi esclusivamente sotto i 20 inliers (Media: 9.0).
- **Potere Discriminante:** È possibile distinguere con elevata precisione una query corretta da una errata impostando una soglia di inliers (es. 30). Questo suggerisce che il numero di inliers è un ottimo proxy per la "reliability" del sistema.

### Distribuzione degli Inliers (LoFTR)
![Istogramma Inliers](Histograms/Netvlad_LoFTR.png)

**Osservazioni:**
- **Netta Separazione delle Distribuzioni**: Le query corrette (verdi) mostrano una distribuzione ampia e spostata verso valori elevati, con una media di 192.9 inliers. Al contrario, le query errate (rosse) sono fortemente concentrate vicino allo zero, con una media di appena 18.2 inliers.

- **Elevata Densità di Corrispondenze**: Rispetto a LightGlue, LoFTR produce un numero di inliers significativamente maggiore (quasi il doppio nelle query corrette). Questo è dovuto alla natura detector-free del metodo, che stabilisce corrispondenze dense sull'intera immagine invece di limitarsi a punti chiave isolati.

- **Affidabilità della Soglia di Confidenza**: La sovrapposizione tra le due distribuzioni è minima. È possibile distinguere quasi perfettamente una query corretta da una errata impostando una soglia (es. 40-50 inliers). Ciò conferma che il numero di inliers di LoFTR è un indicatore di affidabilità (proxy di reliability) estremamente robusto per la verifica geometrica.


### Distribuzione degli Inliers (SuperGlue)
![Istogramma Inliers](Histograms/Netvlad_SuperGlue.png)

**Osservazioni:**
- **Confronto con LoFTR**: Mentre LoFTR produceva una media di inlier molto alta (quasi 200), SuperGlue lavora su punti chiave sparsi (SuperPoint), risultando in una media più bassa (24.6). Tuttavia, la capacità discriminante è identica: le query errate sono confinate in una zona a bassissimo punteggio, rendendo il filtro geometrico molto efficace.

- **Efficienza**: Con un tempo di circa 1.39s per query, SuperGlue rappresenta un eccellente compromesso tra la precisione estrema e la velocità di esecuzione su grandi dataset urbani.

- **Rilevamento Feature**: SuperGlue utilizza una Graph Neural Network per risolvere il problema delle corrispondenze, il che spiega la sua capacità di mantenere una Recall elevata anche con meno "quantità" di match rispetto a metodi dense come LoFTR.

---

## 3. Analisi del Trade-off
Il passaggio dal solo retrieval (NetVLAD) all'aggiunta del re-ranking ha portato un incremento della **Recall@1 del +26.0%**. Tuttavia, questo miglioramento comporta un costo computazionale aggiuntivo dovuto all'estrazione delle feature locali e al calcolo del matching per ogni coppia query-database.