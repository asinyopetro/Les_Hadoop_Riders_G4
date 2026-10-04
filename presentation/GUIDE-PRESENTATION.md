# Guide de présentation — G4 Les_Hadoop_Riders

**Durée :** 8 à 10 minutes  
**Règle :** **2 slides par personne**, dans l’ordre du groupe.  
**Conclusion :** **Wren** (dernière).

---

## Ordre (2 slides chacun)

| Slides | Qui | Contenu |
|--------|-----|---------|
| **1–2** | **Komla** Petro Asinyo | Titre + plan |
| **3–4** | **Kassoum** Dene | 3V e-commerce + HDFS vs local |
| **5–6** | **Joel** Kazoni Tugirimana | YARN + architecture Docker |
| **7–8** | **Forbes** Magène | Déploiement Hub + manipulations HDFS |
| **9–10** | **Frank** A Simo Ngounou | Job π + monitoring UI |
| **11–12** | **Wren** Surprenant-Nicolson | Troubleshooting + **conclusion** |

Temps ≈ **1 min 15 – 1 min 30** par personne.

---

## Avant de commencer

1. Un seul membre clique les slides.
2. Rapport PDF sous la main.
3. Démo live optionnelle : `docker compose up -d` → http://localhost:9870 et :8088
4. Liens :  
   - https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4  
   - https://github.com/asinyopetro/Les_Hadoop_Riders_G4

---

## Quoi dire (par personne)

### Komla (1–2)

« Bonjour, G4 Les_Hadoop_Riders. Cluster Hadoop HDFS + YARN avec Docker.  
Chacun a 2 slides, dans l’ordre. Wren conclut. »

### Kassoum (3–4)

**3 :** e-commerce + Volume / Vélocité / Variété → HDFS stocke, YARN traite.  
**4 :** FS local = 1 machine ; HDFS = blocs + réplication + NameNode.

### Joel (5–6)

**5 :** Client → ResourceManager (orchestre) → NodeManager (exécute).  
**6 :** 1 master + 5 workers, ports 9870 / 8088 / 9000, image `…g4:1.0`.

### Forbes (7–8)

**7 :** `compose up`, `docker ps`, `dfsadmin` → 5 Live ; push Hub (minuscules).  
**8 :** mkdir → put → fsck → head/getmerge → Trash → setrep 2.

### Frank (9–10)

**9 :** job `pi 4 1000` → app `…_0001` SUCCEEDED, π ≈ 3.14.  
**10 :** UI NameNode 5 DN, YARN finished, pas de missing block.

### Wren (11–12) — dernière

**11 :** 3 problèmes (pull, majuscules, download lent) + solutions.  
**12 :** Récap 5 points → Hub + GitHub → « Merci, des questions ? »

---

## Questions filet

| Question | Réponse |
|----------|---------|
| Combien de DataNodes ? | 5 |
| Version Hadoop ? | 3.3.6 |
| Image Hub ? | `leshadoopriders/hadoop-tp-g4:1.0` |
| CSV où ? | `/data/ventes/2026/transactions.csv` |
| Qui alloue les ressources ? | ResourceManager |

---

## Checklist

- [ ] Diaporama testé une fois
- [ ] Chacun connaît **ses 2 slides**
- [ ] Wren prêt pour la fin
- [ ] Parler lentement
