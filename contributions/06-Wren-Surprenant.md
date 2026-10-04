# Wren Surprenant-Nicolson (ENU-L1) — Partie présentation

## Sujet (2–3 min)
**setrep**, monitoring, troubleshooting, Docker Hub.

## Points à dire
1. `hdfs dfs -setrep -w 2 /data/ventes/2026/transactions.csv` → réplication passe à 2.
2. En arrière-plan : NameNode ajuste les copies sur les DataNodes.
3. UI NameNode (espace disque, 5 DN) + YARN (mémoire, SUCCEEDED).
4. Bugs rencontrés :
   - pull image Hub inexistante → `pull_policy: never`
   - tag avec majuscules `G4` refusé → `g4`
   - téléchargement Hadoop trop lent → image `apache/hadoop:3.3.6`
5. Lien Hub : https://hub.docker.com/r/leshadoopriders/hadoop-tp-g4

## À faire avant le 7 oct
- [X] Accepter invite : https://github.com/asinyopetro/Les_Hadoop_Riders_G4/invitations
- [X] Commit + push
- [X] Vérifier la page Hub (Overview + tag 1.0)

## Validation
- [X] Validé par Wren — date : 3 Octobre 2026
