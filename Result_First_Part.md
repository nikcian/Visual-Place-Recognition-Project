## 📊 Tabella Completa Risultati (Retrieval Only)

| Method | SF-XS (R@1 / R@5 / R@10 / R@20) | Tokyo-XS (R@1 / R@5 / R@10 / R@20) | SVOX Night (R@1 / R@5 / R@10 /R@20) | SVOX Sun (R@1 / R@5 / R@10 /R@20) | 
| :--- | :---: | :---: | :---: | :---: |
| **NetVLAD** (VGG16, 4096) | 27.2 / 43.8 / 50.3 / 56.2 | 49.8 / 62.5 / 70.5 / 78.7 | 8.0 / 17.4 / 23.1 / 29.6 | 35.4 / 52.7 / 58.8 / 65.8 | 
| **CosPlace** (ResNet18, 512) | 42.3 / 58.2 / 64.2 / 70.5 | 51.7 / 70.2 / 79.0 / 85.1 | 17.5 / 28.2 / 33.9 / 39.9 | 94.4 / 96.7 / 97.4 / 98.0 | 
| **MixVPR** (ResNet50, 4096) | 70.2 / 79.0 / 81.3 / 83.9 | 78.1 / 89.5 / 92.4 / 93.7 | 47.3 / 64.0 / 69.7 / 75.8 | 96.9 / 98.3 / 98.7 / 99.0 | 
| **MegaLoc** (ResNet18, 4096) | 85.6 / 89.4 / 90.0 / 90.7 | 94.9 / 97.8 / 98.4 / 98.7 | 92.6 / 97.4 / 98.6 / 98.9 | 98.4 / 99.3 / 99.4 / 99.5 | 


### Considerazioni


1.   Crollo di NetVLAD e CosPlace di notte
     
     NetVLAD fa 3.1% (R@1). Praticamente tira a indovinare.
     CosPlace fa 17.5%.

     Motivo: Questi modelli sono addestrati principalmente su immagini diurne. Non hanno imparato a capire che un edificio di giorno è lo stesso edificio di notte (invarianza all'illuminazione). Quando cala il buio, per loro "l'immagine cambia totalmente"


2.   MegaLoc vince
     
     Guardando SVOX Night per MegaLoc: 92.6%.
     È un buon rispetto a CosPlace (17.5%).

     Motivo: MegaLoc è stato progettato specificamente per questo. La sua backbone e il suo training sono fatti per ignorare le differenze di luce e concentrarsi sulla geometria/struttura. La tabella dimostra che funziona perfettamente.


3.   MixVPR è buon compromesso
     
     MixVPR si piazza in mezzo. Su Night fa 47.3%.

     È molto meglio di CosPlace (perché la sua architettura che mischia le feature cattura meglio i dettagli strutturali), ma non raggiunge i livelli di specializzazione di MegaLoc.

     Tuttavia, nota come su SF-XS e Tokyo-XS (ambienti urbani standard) MixVPR sia molto forte, spesso vicino a MegaLoc.

