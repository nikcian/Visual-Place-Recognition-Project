# Report Risultati Sperimentali e Analisi Tecnica

---

## 📍 Dataset: tokyo_xs/test

### Metodo: NetVLAD (Backbone: VGG16 | Dim: 4096)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | 49.8 | 62.5 | 70.5 | 78.7 |
| ip | 49.8 | 62.5 | 70.5 | 78.7 |

### Metodo: CosPlace (Backbone: ResNet50 | Dim: 512)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | 51.7 | 70.2 | 79.0 | 85.1 |
| ip | 51.7 | 70.2 | 79.0 | 85.1 |

### Metodo: MixVPR (Backbone: ResNet50 | Dim: 4096)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | 78.1 | 89.5 | 92.4 | 93.7 |
| ip | 78.1 | 89.5 | 92.4 | 93.7 |

### Metodo: MegaLoc (Backbone: DINOv2 ViT-L/14 | Dim: 8448)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | **94.9** | **97.8** | **98.4** | **98.7** |
| ip | **94.9** | **97.8** | **98.4** | **98.7** |

---

## 📍 Dataset: sf_xs/test

### Metodo: NetVLAD (VGG16 | 4096)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | 27.2 | 43.8 | 50.3 | 56.2 |
| ip | 27.2 | 43.8 | 50.3 | 56.2 |

### Metodo: CosPlace (ResNet50 | 512)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | 42.3 | 58.2 | 64.2 | 70.5 |
| ip | 42.3 | 58.2 | 64.2 | 70.5 |

### Metodo: MixVPR (ResNet50 | 4096)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | 70.2 | 79.0 | 81.3 | 83.9 |
| ip | 70.2 | 79.0 | 81.3 | 83.9 |

### Metodo: MegaLoc (DINOv2 | 8448)
| Distanza | R@1 | R@5 | R@10 | R@20 |
| :--- | :---: | :---: | :---: | :---: |
| l2 | **85.6** | **89.4** | **90.0** | **90.7** |
| ip | **85.6** | **89.4** | **90.0** | **90.7** |

---

## 📍 Dataset: SVOX (test)

### 🌑 Condizione: Night (Cross-Domain Challenge)
| Metodo | Architettura (Backbone) | Dim | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| NetVLAD | VGG16 | 4096 | 8.0 | 17.4 | 23.1 | 29.6 |
| CosPlace | ResNet50 | 512 | 33.4 | 51.9 | 60.8 | 68.3 |
| MixVPR | ResNet50 | 4096 | 62.9 | 79.8 | 84.1 | 88.0 |
| **MegaLoc** | **DINOv2** | **8448** | **97.1** | **98.9** | **99.1** | **99.4** |

### ☀️ Condizione: Sun
| Metodo | Architettura (Backbone) | Dim | R@1 | R@5 | R@10 | R@20 |
| :--- | :--- | :---: | :---: | :---: | :---: |
| NetVLAD | VGG16 | 4096 | 35.4 | 52.7 | 58.8 | 65.8 |
| CosPlace | ResNet50 | 512 | 61.7 | 78.0 | 84.1 | 88.8 |
| MixVPR | ResNet50 | 4096 | 85.4 | 93.0 | 94.7 | 95.9 |
| **MegaLoc** | **DINOv2** | **8448** | **97.3** | **99.3** | **99.5** | **99.6** |

---

# Considerazioni Tecniche sulle Architetture

### Analisi delle Metriche di Distanza: $L^2$ vs Inner Product (IP)
Il confronto diretto tra la distanza Euclidea ($L^2$) e il Prodotto Scalare (IP) rivela risultati identici. Questa equivalenza deriva dalla **normalizzazione $L^2$** applicata ai descrittori globali: proiettando i vettori su un'ipersfera unitaria ($\| \cdot \|_2 = 1$), l'ordinamento dei vicini rimane invariato tra le due metriche. Per l'efficienza computazionale su larga scala, la metrica **Inner Product (IP)** è stata selezionata per gli esperimenti successivi.

### Valutazione Comparativa delle Backbone
1. **MegaLoc (DINOv2 ViT):** Rappresenta lo stato dell'arte. L'uso di una backbone **Vision Transformer** pre-addestrata con metodo self-supervised (DINOv2) permette di estrarre feature semantiche insensibili ai cambiamenti di luce. Questo giustifica l'eccezionale Recall@1 del 97.1% in notturna.
2. **MixVPR (ResNet50):** Utilizza una backbone solida accoppiata a un'architettura di **Feature Mixing**. A differenza del pooling standard, MixVPR preserva le relazioni spaziali, superando NetVLAD e CosPlace specialmente in contesti urbani complessi come SF-XS.
3. **CosPlace (ResNet50):** Ottimizzato per la compressione, produce un descrittore di sole **512 dimensioni**. Nonostante l'estrema leggerezza, supera NetVLAD grazie a un training set massivo e una loss orientata alla robustezza prospettica.
4. **NetVLAD (VGG16):** L'architettura più datata. La backbone VGG16 e l'aggregazione VLAD mostrano evidenti limiti nel gestire il dominio notturno (R@1: 8.0%), evidenziando la difficoltà delle CNN classiche nel generalizzare tra domini diversi senza meccanismi di attenzione o mixing avanzati.



### Conclusioni sul Retrieval Globale
L'analisi conferma che mentre modelli moderni come MegaLoc sono estremamente precisi, i modelli più leggeri beneficerebbero significativamente di una **Fase 5.2 di Image Matching**. La crescita dei valori R@10 e R@20 indica che l'informazione corretta è quasi sempre presente nei primi candidati, pronta per essere raffinata tramite il conteggio degli *inliers* geometrici.
