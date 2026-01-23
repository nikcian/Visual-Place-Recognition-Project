# 6.1 Analisi e Selezione della Soglia Adattiva (LoFTR)

In questa sezione determiniamo la soglia ottimale di inlier ($\tau$) per distinguere le query "Facili" da quelle "Difficili". L'obiettivo è massimizzare l'**F2-Score**, una metrica che privilegia la capacità di recuperare match corretti (Recall) mantenendo però un significativo risparmio computazionale.

### 6.1.1 Analisi su SVOX Sun Train (Scenario Diurno)

Analizziamo il comportamento del sistema sul dataset di training diurno.

![Trade-off Recall vs Saving Sun](grafici_tau/tau_svox_sun_train_loftr.png)
*Fig 6.1: Trade-off su SVOX Sun Train. Il picco dell'F2-Score identifica il miglior bilanciamento.*

**Tabella di Trade-off (SVOX Sun Train)**

| Tau ($\tau$) | Recall@1 | Saving | F2-Score | Note |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 29.63% | 93.99% | 0.3434 | |
| 5 | 29.78% | 92.66% | 0.3445 | |
| 10 | 42.84% | 52.74% | 0.4451 | |
| **12** | **46.49%** | **40.58%** | **0.4517** | ⭐ **BEST** |
| 15 | 48.88% | 32.91% | 0.4456 | |
| 20 | 50.28% | 29.48% | 0.4406 | |
| 25 | 50.56% | 28.29% | 0.4368 | |

**Analisi:**
Il punto di ottimo matematico si trova a **$\tau = 12$**.
* A questo valore, il sistema ottiene una Recall del **46.49%** mantenendo un risparmio del **40.58%**.
* Soglie inferiori (<10) hanno un risparmio altissimo (>90%) ma una Recall insufficiente (~29%), indicando che fidarsi troppo ciecamente di pochi inlier porta a perdere molti match.
* Soglie superiori (>20) portano guadagni marginali di Recall a fronte di un crollo del risparmio sotto il 30%.

---

### 6.1.2 Analisi su SVOX Night Train (Scenario Notturno)

Lo scenario notturno rappresenta il "caso peggiore", dove il retrieval globale è meno affidabile e i match geometrici sono più scarsi.

![Trade-off Recall vs Saving Night](grafici_tau/tau_svox_night_train_loftr.png)
*Fig 6.2: Trade-off su SVOX Night Train. Si nota la necessità di abbassare la soglia per mantenere un minimo di efficienza.*

**Tabella di Trade-off (SVOX Night Train)**

| Tau ($\tau$) | Recall@1 | Saving | F2-Score | Note |
| :--- | :--- | :--- | :--- | :--- |
| 0 | 3.13% | 94.12% | 0.0389 | |
| 5 | 3.28% | 92.37% | 0.0406 | |
| **10** | **11.25%** | **21.05%** | **0.1241** | ⭐ **BEST** |
| 15 | 13.39% | 3.89% | 0.0899 | |
| 20 | 13.53% | 2.68% | 0.0748 | |

**Analisi e Scelta della Soglia Operativa:**
* Il picco dell'F2-Score si trova a **$\tau = 10$**.
* Si osserva una criticità fondamentale: passando da $\tau=10$ a $\tau=15$, il **risparmio crolla dal 21% al 3.89%**. Questo accade perché di notte quasi tutti i match corretti hanno un numero di inlier molto basso (tra 10 e 15).
* Per evitare che il sistema degradi in un re-ranking totale (Saving ~0%), siamo costretti a fermarci a **10**.

**Decisione Finale:**
Sebbene l'ottimo per il giorno sia 12, scegliamo **$\tau = 10$** come soglia globale unica. È il valore ottimale per la notte (il collo di bottiglia del sistema) ed è estremamente vicino all'ottimo diurno, garantendo robustezza in tutte le condizioni.

---

# 6.2 Validazione della Soglia (SF-XS Val)

Validiamo la scelta di **$\tau = 10$** sul dataset di validazione San Francisco (SF-XS Val), mai visto durante l'analisi.

![Validazione SF-XS](grafici_tau/validation_tau_sf_xs_val_loftr.png)

**Risultati Validazione**

| Metodo | Tau Scelto | Recall@1 | Risparmio (Saving) | Note |
| :--- | :--- | :--- | :--- | :--- |
| **LoFTR** | **10** | **52.70%** | **78.49%** | ⬅️ **CHOSEN** |

**Discussione:**
La validazione conferma l'efficacia della soglia. Su SF-XS, $\tau=10$ permette un **risparmio eccezionale del 78.49%**. Questo indica che in questo ambiente urbano il Global Retrieval (NetVLAD) è spesso corretto e LoFTR lo conferma facilmente superando i 10 inlier, permettendo al sistema di saltare il re-ranking quasi nell'80% dei casi.

---

# 6.3 Valutazione sui Test Set (SVOX)

Applichiamo ora la soglia congelata **$\tau = 10$** ai dataset di test di Pittsburgh.

### 6.3.1 SVOX Sun Test

![Test SVOX Sun](grafici_tau/test_tau_svox_sun_loftr.png)

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **LoFTR** | **10** | **46.84%** | **63.48%** |

**Analisi:**
Il sistema si comporta in modo eccellente di giorno, garantendo un **risparmio del 63.48%** e una Recall del 46.84%. Rispetto al training set, l'efficienza è addirittura migliorata, confermando che la soglia 10 non è troppo restrittiva per le immagini diurne.

### 6.3.2 SVOX Night Test

![Test SVOX Night](grafici_tau/test_tau_svox_night_loftr.png)

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **LoFTR** | **10** | **20.78%** | **26.42%** |

**Analisi:**
Nello scenario notturno, il sistema si adatta automaticamente alla difficoltà. Il risparmio scende al **26.42%**, poiché il sistema riconosce l'incertezza e attiva il re-ranking per il 74% delle query. Questo comportamento protettivo permette di mantenere la Recall al **20.78%**; se avessimo forzato un risparmio più alto, la recall sarebbe crollata.

---

# 6.4 Valutazione su Test Set Urbani (SF & Tokyo)

Verifichiamo la capacità di generalizzazione geografica della soglia **$\tau = 10$**.

### 6.4.1 SF-XS Test

![Test SF-XS](grafici_tau/test_tau_sf_xs_loftr.png)

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **LoFTR** | **10** | **33.30%** | **76.99%** |

**Analisi:**
Su San Francisco Test, otteniamo un **risparmio massiccio del 76.99%**. Il sistema identifica correttamente che la maggior parte delle query sono "Facili" per NetVLAD in questo dataset, riducendo drasticamente i tempi di latenza senza bisogno di ri-addestramento.

### 6.4.2 Tokyo-XS Test

![Test Tokyo-XS](grafici_tau/test_tau_tokyo_loftr.png)

| Metodo | Tau ($\tau$) | Recall@1 | Risparmio (Saving) |
| :--- | :--- | :--- | :--- |
| **LoFTR** | **10** | **56.83%** | **73.20%** |

**Analisi:**
Anche a Tokyo, un ambiente visivamente molto denso e diverso dagli USA, la soglia 10 si rivela robusta. Il **risparmio è del 73.20%** con una Recall molto alta del **56.83%**. Questo dimostra l'universalità del parametro geometrico: 10 inlier sono una "firma di correttezza" valida trasversalmente a diverse città.

---

## 6.5 Conclusioni Finali: Adaptive Re-ranking ($\tau=10$)

La tabella seguente riassume l'impatto della strategia adattiva con $\tau=10$ sui tre dataset di test principali.

| Dataset | Adaptive Recall@1 | Risparmio Tempo | Valutazione |
| :--- | :--- | :--- | :--- |
| **SF-XS Test** | 33.30% | **76.99%** | Alta Efficienza |
| **Tokyo-XS** | 56.83% | **73.20%** | Ottimo Bilanciamento |
| **SVOX Sun** | 46.84% | **63.48%** | Risparmio Significativo |
| **SVOX Night** | 20.78% | **26.42%** | Adattamento alla Difficoltà |

**Sintesi:**
L'introduzione della soglia adattiva **$\tau=10$** ha trasformato il sistema:
1.  **Velocità:** In scenari urbani standard (giorno), il sistema è **4 volte più veloce** (risparmio ~75%) rispetto al re-ranking esaustivo.
2.  **Intelligenza:** Il sistema non applica ciecamente l'ottimizzazione; quando le condizioni si fanno critiche (Notte), sacrifica il risparmio per proteggere la precisione.
3.  **Generalizzazione:** Il parametro non richiede tuning specifico per ogni città, rendendo l'approccio scalabile per applicazioni reali.