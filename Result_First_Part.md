## 📊 Tabella Completa Risultati (Retrieval Only)

| Method | SF-XS (R@1 / R@5 / R@10 / R@20) | Tokyo-XS (R@1 / R@5 / R@10 / R@20) | SVOX Night (R@1 / R@5 / R@10 /R@20) | SVOX Sun (R@1 / R@5 / R@10 /R@20) | SVOX Rain (R@1 / R@5 / R@10 /R@20) | SVOX Snow (R@1 / R@5 / R@10 /R@20) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **NetVLAD** (VGG16, 4096) | 27.2 / 43.8 / 50.3 / 56.2 | 49.8 / 62.5 / 70.5 / 78.7 | 3.1 / 9.0 / 12.1 / 17.8 | 73.0 / 85.1 / 88.7 / 91.7 | 38.0 / 51.6 / 58.0 / 64.3 | 42.2 / 59.9 / 64.4 / 70.4 |
| **CosPlace** (ResNet18, 512) | 42.3 / 58.2 / 64.2 / 70.5 | 51.7 / 70.2 / 79.0 / 85.1 | 17.5 / 28.2 / 33.9 / 39.9 | 94.4 / 96.7 / 97.4 / 98.0 | 70.7 / 82.3 / 85.6 / 88.3 | 76.2 / 84.3 / 84.7 / 89.5 |
| **MixVPR** (ResNet50, 4096) | 70.2 / 79.0 / 81.3 / 83.9 | 78.1 / 89.5 / 92.4 / 93.7 | 47.3 / 64.0 / 69.7 / 75.8 | 96.9 / 98.3 / 98.7 / 99.0 | 88.3 / 94.5 / 96.4 / 97.6 | 93.4 / 96.6 / 96.8 / 97.5 |
| **MegaLoc** (ResNet18, 4096) | 85.6 / 89.4 / 90.0 / 90.7 | 94.9 / 97.8 / 98.4 / 98.7 | 92.6 / 97.4 / 98.6 / 98.9 | 98.4 / 99.3 / 99.4 / 99.5 | 98 / 99.5 / 99.7 / 99.7 | 98.3 / 99.3 / 99.4 / 99.6 |


### Considerazioni


1.   Crollo di NetVLAD e CosPlace di notte
     
     NetVLAD fa 3.1% (R@1). Praticamente tira a indovinare.
     CosPlace fa 17.5%.

     Motivo: Questi modelli sono addestrati principalmente su immagini diurne. Non hanno imparato a capire che un edificio di giorno è lo stesso edificio di notte (invarianza all'illuminazione). Quando cala il buio, per loro "l'immagine cambia totalmente"


2.   MegaLoc vince
     
     Guardando SVOX Night per MegaLoc: 92.6%.
     È un buon rispetto a CosPlace (17.5%).

     Motivo: MegaLoc è stato progettato specificamente per questo. La sua backbone e il suo training sono fatti per ignorare le differenze di luce e concentrarsi sulla geometria/struttura. La tabella dimostra che funziona perfettamente.

     Anche su Rain e Snow, MegaLoc domina (98%), dimostrando di essere il modello più "robusto" (Cross-Domain).

3.   MixVPR è buon compromesso
     
     MixVPR si piazza in mezzo. Su Night fa 47.3%.

     È molto meglio di CosPlace (perché la sua architettura che mischia le feature cattura meglio i dettagli strutturali), ma non raggiunge i livelli di specializzazione di MegaLoc.

     Tuttavia, nota come su SF-XS e Tokyo-XS (ambienti urbani standard) MixVPR sia molto forte, spesso vicino a MegaLoc.

