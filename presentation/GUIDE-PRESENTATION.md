# Guide de présentation — G4 Les_Hadoop_Riders

**Durée :** 8 à 10 minutes  
**Fichier PPT :** `PRESENTATION-G4-Les_Hadoop_Riders.pptx`  
**Date cible :** présentation orale (ex. 8 oct.)

Objectif de ce guide : savoir **qui parle**, **quoi dire**, et **que répondre** si le prof pose une question.

---

## Ordre de passage (résumé)

| Slides | Qui | Temps |
|--------|-----|-------|
| 1–2 | **Komla** Petro Asinyo | ~1 min |
| 3 | **Kassoum** Dene | ~1 min |
| 4 | **Joel** Kazoni Tugirimana | ~1 min |
| 5 | **Forbes** Magène | ~1 min |
| 6–7 | **Frank** A Simo Ngounou | ~1 min 30 |
| 8 | **Wren** Surprenant-Nicolson | ~1 min 30 |
| 9 | **Forbes** Magène | ~1 min |
| 10 | **Joel** Kazoni Tugirimana | ~1 min |
| 11 | **Kassoum** Dene | ~1 min |
| 12 | **Komla** Petro Asinyo | ~45 s + questions |

Chaque slide a déjà le **nom du présentateur en bas**.

Astuce PowerPoint : Mode Présentateur → les **notes** sont déjà dans le fichier (clic droit slide → Notes).

---

## Avant de commencer (groupe)

1. Ouvrir le PPT et se mettre d’accord sur qui clique (un seul « clicker »).
2. Avoir le rapport PDF sous la main (captures si le prof demande une preuve).
3. Si démo live possible :
   - `docker compose up -d`
   - UI : http://localhost:9870 et http://localhost:8088
4. Liens à connaître :
   - Hub : https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4
   - GitHub : https://github.com/asinyopetro/Les_Hadoop_Riders_G4

---

## Slide par slide — quoi dire

### Slide 1 — Titre (Komla)

**Dire :**  
« Bonjour, nous sommes le groupe G4 Les_Hadoop_Riders. On présente notre projet : un cluster Hadoop HDFS + YARN déployé avec Docker. »

**Ne pas faire :** lire toute la liste des noms lentement.

---

### Slide 2 — Plan (Komla)

**Dire :**  
« On commence par le contexte théorique, puis l’architecture Docker, les manipulations HDFS, un job YARN, et on termine par le monitoring et les problèmes rencontrés. »

Passe la parole à Kassoum.

---

### Slide 3 — E-commerce et 3V (Kassoum)

**Dire (environ 60 s) :**  
« On a choisi l’e-commerce : une chaîne de magasins avec tickets de caisse, logs web et stocks.  
- Volume : beaucoup de données sur plusieurs années.  
- Vélocité : les commandes arrivent en continu.  
- Variété : CSV, JSON, logs, images.  
HDFS sert à stocker, YARN à traiter. »

**Question possible :** Pourquoi pas une base SQL seule ?  
**Réponse courte :** SQL ok pour données structurées ; ici volume + variété + fichiers → stockage distribué type HDFS plus adapté.

---

### Slide 4 — HDFS vs FS classique (Joel)

**Dire :**  
« Sur un disque local, le fichier est sur une machine.  
Sur HDFS, il est découpé en blocs, répliqués sur plusieurs DataNodes. Le NameNode garde les noms et l’emplacement des blocs. Ça tolère mieux les pannes. »

**Question possible :** C’est quoi un bloc ?  
**Réponse :** Un morceau du fichier (souvent 128 Mo). Notre CSV est petit → 1 seul bloc, c’est normal.

---

### Slide 5 — YARN RM / NM (Forbes)

**Dire :**  
« Quand on lance un job : le ResourceManager (master) reçoit la demande et alloue des ressources.  
Le NodeManager (sur chaque worker) démarre les conteneurs sur sa machine.  
RM orchestre, NM exécute. »

**Question possible :** Et l’ApplicationMaster ?  
**Réponse :** C’est le « chef » du job ; le RM aide à le démarrer, puis l’AM demande des conteneurs pour les maps/reduces.

---

### Slides 6–7 — Architecture + Hub (Frank)

**Slide 6 — Dire :**  
« Six conteneurs : master (NameNode + ResourceManager) et cinq workers (DataNode + NodeManager).  
Ports : 9870 HDFS, 8088 YARN, 9000 RPC. »

**Slide 7 — Dire :**  
« On lance avec `docker compose up --build -d`.  
`dfsadmin -report` montre 5 Live datanodes.  
Image publiée : `leshadoopriders/hadoop-tp-g4:1.0`. »

**Question possible :** Pourquoi `g4` en minuscules ?  
**Réponse :** Docker Hub refuse les majuscules dans le nom du dépôt.

---

### Slide 8 — Manipulations HDFS (Wren)

**Dire (suivre l’ordre) :**  
1. Création `/data/ventes/2026` + droits + upload CSV  
2. `fsck` / `stat` → HEALTHY, réplication 3  
3. Lecture `head`, puis `getmerge`  
4. Suppression avec Trash  
5. `setrep -w 2` → réplication à 2  

**Question possible :** À quoi sert Trash ?  
**Réponse :** Évite la suppression définitive immédiate ; le fichier va dans `.Trash`. `-skipTrash` force la suppression.

---

### Slide 9 — Job π (Forbes)

**Dire :**  
« On a lancé l’exemple MapReduce `pi` avec 4 maps et 1000 samples.  
Application `application_1791039798429_0001`, état SUCCEEDED, π ≈ 3.14.  
Visible dans l’UI YARN. »

**Question possible :** Pourquoi π ?  
**Réponse :** Exemple officiel Hadoop, simple à lancer, prouve que YARN exécute bien un job.

---

### Slide 10 — Monitoring (Joel)

**Dire :**  
« UI NameNode : 5 DataNodes, pas de missing block.  
UI YARN : job finished / succeeded, avec mémoire et vcores.  
Avec setrep, le NameNode met à jour la cible de réplication. »

---

### Slide 11 — Troubleshooting (Kassoum)

**Dire les 3 points :**  
1. Compose voulait pull une image pas encore publiée → `pull_policy: never`  
2. Tag avec majuscules refusé → tout en minuscules  
3. Download Apache trop lent → base `apache/hadoop:3.3.6`

---

### Slide 12 — Conclusion (Komla)

**Dire :**  
« En résumé : cluster 1+5 opérationnel, HDFS manipulé, job π réussi, image sur Docker Hub. Merci, des questions ? »

---

## Questions « filet de sécurité » (tout le monde)

| Question | Réponse courte |
|----------|----------------|
| Combien de DataNodes ? | 5 |
| Quelle version Hadoop ? | 3.3.6 |
| Où est le CSV ? | `/data/ventes/2026/transactions.csv` |
| Lien Hub ? | `leshadoopriders/hadoop-tp-g4` |
| Différence HDFS / local ? | Blocs + réplication + NameNode |
| Qui alloue les ressources ? | ResourceManager |

Si tu ne sais pas : « On a documenté ça dans le rapport section X » — mieux que d’inventer.

---

## Timing si on dépasse

Couper dans cet ordre :
1. Détails du slide 10 (métriques exactes)
2. Un des 3 problèmes du slide 11
3. Ne pas relire les commandes du slide 7 en entier

Ne jamais couper : 3V, HDFS vs local, RM/NM, 5 workers, job SUCCEEDED.

---

## Checklist jour J

- [ ] PPT ouvert, mode diaporama testé une fois
- [ ] Chacun a relu **ses** slides + notes
- [ ] Un membre prêt à ouvrir 9870 / 8088 si demandé
- [ ] Rapport PDF accessible
- [ ] Parler lentement, regarder la salle, pas le mur
