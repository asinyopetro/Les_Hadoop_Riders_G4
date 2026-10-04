# Guide de présentation — G4 Les_Hadoop_Riders

**Durée :** 8 à 10 minutes  
**Fichier PPT :** `PRESENTATION-G4-Les_Hadoop_Riders.pptx`  
**Règle :** le nom du présentateur est en bas de chaque slide.  
**Conclusion :** **Wren** (dernière personne du groupe).

---

## Ordre de passage

| Slides | Qui | Temps |
|--------|-----|-------|
| 1–2 | **Komla** Petro Asinyo | ~1 min |
| 3 | **Kassoum** Dene | ~1 min |
| 4 | **Joel** Kazoni Tugirimana | ~1 min |
| 5 | **Forbes** Magène | ~1 min |
| 6–7 | **Frank** A Simo Ngounou | ~1 min 30 |
| 8 | **Wren** Surprenant-Nicolson | ~1 min 15 |
| 9 | **Forbes** Magène | ~1 min |
| 10 | **Joel** Kazoni Tugirimana | ~1 min |
| 11 | **Kassoum** Dene | ~1 min |
| 12 | **Wren** Surprenant-Nicolson (conclusion) | ~45 s + questions |

Astuce : Mode Présentateur → lire les **notes** sous chaque slide.

---

## Avant de commencer

1. Un seul membre clique les slides.
2. Avoir le rapport PDF sous la main.
3. Si démo live : `docker compose up -d` puis http://localhost:9870 et :8088
4. Liens :
   - https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4
   - https://github.com/asinyopetro/Les_Hadoop_Riders_G4

---

## Slide par slide

### 1–2 — Komla (intro + plan)

**Dire :**  
« Bonjour, G4 Les_Hadoop_Riders. On présente un cluster Hadoop HDFS + YARN avec Docker.  
Objectif : déployer, manipuler HDFS, lancer un job YARN, publier l’image.  
Voici le plan — Wren fera la conclusion. »

---

### 3 — Kassoum (3V)

**Dire :**  
Contexte e-commerce (ventes, logs, stocks).  
Volume / Vélocité / Variété avec un exemple chacun.  
Finir : HDFS stocke, YARN traite.

**Q :** Pourquoi pas seulement SQL ?  
**R :** SQL ok en structuré ; ici volume + variété de fichiers → HDFS plus adapté.

---

### 4 — Joel (HDFS)

**Dire :**  
Local = une machine. HDFS = blocs + réplication + NameNode.  
Pointer le schéma sur le slide.

**Q :** C’est quoi un bloc ?  
**R :** Morceau du fichier (souvent 128 Mo). Notre CSV est petit → 1 bloc.

---

### 5 — Forbes (YARN)

**Dire :**  
Client → ResourceManager (orchestre) → NodeManagers (exécutent).  
Montrer la capture UI.

**Q :** ApplicationMaster ?  
**R :** Chef du job ; le RM aide à le démarrer.

---

### 6–7 — Frank (archi + Hub)

**Dire :**  
1 master (NN+RM) + 5 workers (DN+NM). Ports 9870 / 8088 / 9000.  
Commandes : compose up, docker ps, dfsadmin → 5 Live.  
Push Hub `leshadoopriders/hadoop-tp-g4:1.0` (minuscules).

---

### 8 — Wren (HDFS pratique)

**Dire :** les 5 étapes du slide (mkdir → put → fsck → merge/trash → setrep).  
Fichier petit = 1 bloc, c’est normal.  
*(Tu reviens à la fin pour conclure.)*

---

### 9 — Forbes (job π)

**Dire :** commande pi 4 1000, app `…_0001`, SUCCEEDED, π ≈ 3.14.  
Preuve que YARN marche.

---

### 10 — Joel (monitoring)

**Dire :** UI NameNode 5 DN, pas de missing block ; YARN finished ; setrep met à jour la cible.

---

### 11 — Kassoum (troubles)

**Dire :** les 3 problèmes (pull, majuscules, download lent) + solutions.  
Puis : « Je passe la parole à Wren pour conclure. »

---

### 12 — Wren (conclusion — dernière)

**Dire :**  
« Pour conclure : cluster 1+5 OK, HDFS manipulé, job π réussi, image sur Docker Hub, rapport et code livrés.  
Merci, des questions ? »

Ouvrir les liens Hub / GitHub si demandé.

---

## Questions filet (tout le monde)

| Question | Réponse |
|----------|---------|
| Combien de DataNodes ? | 5 |
| Version Hadoop ? | 3.3.6 |
| Image Hub ? | `leshadoopriders/hadoop-tp-g4:1.0` |
| Où est le CSV ? | `/data/ventes/2026/transactions.csv` |
| Qui alloue les ressources ? | ResourceManager |

---

## Checklist jour J

- [ ] PPT ouvert une fois en mode diaporama
- [ ] Chacun a relu **ses** slides + notes
- [ ] Wren prêt pour la **conclusion**
- [ ] Rapport PDF accessible
- [ ] Parler lentement, regarder la salle
